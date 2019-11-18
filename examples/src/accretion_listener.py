"""
This is an example showing how you could use rhodes to build Accretion's listener workflow.

The JSON definition can be found in this directory in the "accretion_listener.json" file.

https://accretion.readthedocs.io/en/latest/src/overview.html
"""
from rhodes.choice_rules import VariablePath, all_
from rhodes.states import Choice, Fail, Parameters, StateMachine, Succeed, Task, Wait
from rhodes.structures import JsonPath


def build() -> StateMachine:

    workflow = StateMachine(Comment="Replication Listener")

    event_filter = workflow.start_with(
        Task("Filter", Resource="arn:aws:lambda:us-east-1:123456789012:function:event-filter", ResultPath="$")
    )
    skip_check = event_filter.then(Choice("ShouldProcess"))
    skip_check.else_(Succeed("IgnoreEvent", Comment="Ignore this event"))

    locate_artifact = skip_check.if_(VariablePath("$.ProcessEvent") == True).then(
        Task(
            "LocateArtifact",
            Resource="arn:aws:lambda:us-east-1:123456789012:function:artifact-locator",
            ResultPath="$.Artifact",
        )
    )
    artifact_check = locate_artifact.then(Choice("ArtifactCheck"))

    publisher = artifact_check.if_(VariablePath("$.Artifact.Found") == True).then(
        Task(
            "PublishNewVersion",
            Resource="arn:aws:lambda:us-east-1:123456789012:function:layer-version-publisher",
            ResultPath="$.Layer",
        )
    )
    publisher.then(
        Task(
            "Notify",
            Resource="arn:aws:states:::sns:publish",
            Parameters=Parameters(
                TopicArn="arn:aws:sns:us-east-1:123456789012:accretion-notify", Message=JsonPath("$.Layer")
            ),
        )
    ).end()

    artifact_check.if_(
        all_(VariablePath("$.Artifact.Found") == False, VariablePath("$.Artifact.ReadAttempts") > 15)
    ).then(Fail("ReplicationTimeout", Error="Timed out waiting for artifact to replicate"))

    waiter = artifact_check.else_(Wait("WaitForReplication", Seconds=60))
    waiter.then(locate_artifact)

    return workflow
