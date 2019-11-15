"""Complex state machine definition tests."""
import pytest

from rhodes import StateMachine, choice_rules
from rhodes.exceptions import InvalidDefinitionError
from rhodes.states import Choice, Fail, Map, Parallel, Pass, State, Succeed, Task, Wait
from rhodes.structures import Variable

from ..unit_test_helpers import state_machine_body

pytestmark = [pytest.mark.local, pytest.mark.functional]

PARSE_REQUIREMENTS_RESOURCE = "arn:aws:lambda:us-east-1:123456789012:function:parse-requirements"
BUILD_PYTHON_36_RESOURCE = "arn:aws:lambda:us-east-1:123456789012:function:build-py36"
BUILD_PYTHON_37_RESOURCE = "arn:aws:lambda:us-east-1:123456789012:function:build-py37"


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

    expected = state_machine_body("accretion_builder")
    actual = test.to_dict()
    assert actual == expected


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
    select_language.if_(Variable("$.Language") == "python").then_(build_python)
    select_language.else_(unknown_language)

    build_python.end()

    expected = state_machine_body("accretion_builder")
    actual = test.to_dict()
    assert actual == expected
