"""Complex state machine definition tests."""
import pytest

from rhodes import StateMachine, choice_rules
from rhodes.choice_rules import VariablePath, all_
from rhodes.states import Choice, Fail, Parallel, Parameters, Succeed, Task, Wait
from rhodes.structures import JsonPath

from ..unit_test_helpers import compare_state_machine

pytestmark = [pytest.mark.local, pytest.mark.functional]

PARSE_REQUIREMENTS_RESOURCE = "arn:aws:lambda:us-east-1:123456789012:function:parse-requirements"
BUILD_PYTHON_36_RESOURCE = "arn:aws:lambda:us-east-1:123456789012:function:build-py36"
BUILD_PYTHON_37_RESOURCE = "arn:aws:lambda:us-east-1:123456789012:function:build-py37"
EVENT_FILTER_RESOURCE = "arn:aws:lambda:us-east-1:123456789012:function:event-filter"
ARTIFACT_LOCATOR_RESOURCE = "arn:aws:lambda:us-east-1:123456789012:function:artifact-locator"
LAYER_VERSION_PUBLISHER_RESOURCE = "arn:aws:lambda:us-east-1:123456789012:function:layer-version-publisher"
NOTIFY_TOPIC = "arn:aws:sns:us-east-1:123456789012:accretion-notify"


def test_accretion_builder():
    test = StateMachine(
        Comment="Artifact Builder",
        StartAt="ParseRequirements",
        States=dict(
            ParseRequirements=Task("ParseRequirements", Resource=PARSE_REQUIREMENTS_RESOURCE, Next="SelectLanguage"),
            SelectLanguage=Choice(
                "SelectLanguage",
                Choices=[choice_rules.StringEquals(Variable="$.Language", Value="python", Next="BuildPython")],
                Default="UnknownLanguage",
            ),
            UnknownLanguage=Fail("UnknownLanguage", Cause="Invalid language"),
            BuildPython=Parallel(
                "BuildPython",
                Branches=[
                    StateMachine(
                        StartAt="BuildPython36",
                        States=dict(BuildPython36=Task("BuildPython36", Resource=BUILD_PYTHON_36_RESOURCE, End=True)),
                    ),
                    StateMachine(
                        StartAt="BuildPython37",
                        States=dict(BuildPython37=Task("BuildPython37", Resource=BUILD_PYTHON_37_RESOURCE, End=True)),
                    ),
                ],
                ResultPath="$.BuildResults",
                End=True,
            ),
        ),
    )

    compare_state_machine("accretion_builder", test)


def test_accretion_builder_new_1():
    parse_requirements = Task("ParseRequirements", Resource=PARSE_REQUIREMENTS_RESOURCE)

    build_python = Parallel("BuildPython", ResultPath="$.BuildResults")

    build_python_36 = build_python.add_branch()
    build_python_36.start_with(Task("BuildPython36", Resource=BUILD_PYTHON_36_RESOURCE)).end()

    build_python_37 = build_python.add_branch()
    build_python_37.start_with(Task("BuildPython37", Resource=BUILD_PYTHON_37_RESOURCE)).end()

    unknown_language = Fail("UnknownLanguage", Cause="Invalid language")

    test = StateMachine(Comment="Artifact Builder")
    select_language = test.start_with(parse_requirements).then(Choice("SelectLanguage"))

    # TODO: Auto-add children to parent if they were added before the choice was added to parent
    # TODO: Add Choice.elseif_() ?
    select_language.if_(VariablePath("$.Language") == "python").then(build_python)
    select_language.else_(unknown_language)

    build_python.end()

    compare_state_machine("accretion_builder", test)


def test_accretion_listener():

    test = StateMachine(
        Comment="Replication Listener",
        StartAt="Filter",
        States={
            "Filter": Task("Filter", Resource=EVENT_FILTER_RESOURCE, ResultPath="$", Next="ShouldProcess"),
            "ShouldProcess": Choice(
                "ShouldProcess",
                Choices=[choice_rules.BooleanEquals(Variable="$.ProcessEvent", Value=True, Next="LocateArtifact")],
                Default="IgnoreEvent",
            ),
            "IgnoreEvent": Succeed("IgnoreEvent", Comment="Ignore this event"),
            "LocateArtifact": Task(
                "LocateArtifact", Resource=ARTIFACT_LOCATOR_RESOURCE, ResultPath="$.Artifact", Next="ArtifactCheck"
            ),
            "ArtifactCheck": Choice(
                "ArtifactCheck",
                Choices=[
                    choice_rules.BooleanEquals(Variable="$.Artifact.Found", Value=True, Next="PublishNewVersion"),
                    choice_rules.And(
                        Rules=[
                            choice_rules.BooleanEquals(Variable="$.Artifact.Found", Value=False),
                            choice_rules.NumericGreaterThan(Variable="$.Artifact.ReadAttempts", Value=15),
                        ],
                        Next="ReplicationTimeout",
                    ),
                ],
                Default="WaitForReplication",
            ),
            "ReplicationTimeout": Fail("ReplicationTimeout", Error="Timed out waiting for artifact to replicate"),
            "WaitForReplication": Wait("WaitForReplication", Seconds=60, Next="LocateArtifact"),
            "PublishNewVersion": Task(
                "PublishNewVersion", Resource=LAYER_VERSION_PUBLISHER_RESOURCE, ResultPath="$.Layer", Next="Notify"
            ),
            "Notify": Task(
                "Notify",
                Resource="arn:aws:states:::sns:publish",
                Parameters=Parameters(**{"TopicArn": NOTIFY_TOPIC, "Message.$": "$.Layer"}),
                End=True,
            ),
        },
    )

    compare_state_machine("accretion_listener", test)


def test_accretion_listener_new_1():

    test = StateMachine(Comment="Replication Listener")

    event_filter = test.start_with(Task("Filter", Resource=EVENT_FILTER_RESOURCE, ResultPath="$"))
    skip_check = event_filter.then(Choice("ShouldProcess"))
    skip_check.else_(Succeed("IgnoreEvent", Comment="Ignore this event"))

    locate_artifact = skip_check.if_(VariablePath("$.ProcessEvent") == True).then(
        Task("LocateArtifact", Resource=ARTIFACT_LOCATOR_RESOURCE, ResultPath="$.Artifact")
    )
    artifact_check = locate_artifact.then(Choice("ArtifactCheck"))

    publisher = artifact_check.if_(VariablePath("$.Artifact.Found") == True).then(
        Task("PublishNewVersion", Resource=LAYER_VERSION_PUBLISHER_RESOURCE, ResultPath="$.Layer")
    )
    publisher.then(
        Task(
            "Notify",
            Resource="arn:aws:states:::sns:publish",
            Parameters=Parameters(TopicArn=NOTIFY_TOPIC, Message=JsonPath("$.Layer")),
        )
    ).end()

    artifact_check.if_(
        all_(VariablePath("$.Artifact.Found") == False, VariablePath("$.Artifact.ReadAttempts") > 15)
    ).then(Fail("ReplicationTimeout", Error="Timed out waiting for artifact to replicate"))

    waiter = artifact_check.else_(Wait("WaitForReplication", Seconds=60))
    waiter.then(locate_artifact)

    compare_state_machine("accretion_listener", test)
