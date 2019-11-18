"""
This is an example showing how you could use rhodes to build Accretion's artifact builder workflow.

The JSON definition can be found in this directory in the "accretion_builder.json" file.

https://accretion.readthedocs.io/en/latest/src/overview.html
"""
from rhodes.choice_rules import VariablePath
from rhodes.states import Choice, Fail, Parallel, StateMachine, Task


def build() -> StateMachine:
    parse_requirements = Task(
        "ParseRequirements", Resource="arn:aws:lambda:us-east-1:123456789012:function:parse-requirements"
    )

    build_python = Parallel("BuildPython", ResultPath="$.BuildResults")

    build_python_36 = build_python.add_branch()
    build_python_36.start_with(
        Task("BuildPython36", Resource="arn:aws:lambda:us-east-1:123456789012:function:build-py36")
    ).end()

    build_python_37 = build_python.add_branch()
    build_python_37.start_with(
        Task("BuildPython37", Resource="arn:aws:lambda:us-east-1:123456789012:function:build-py37")
    ).end()

    unknown_language = Fail("UnknownLanguage", Cause="Invalid language")

    workflow = StateMachine(Comment="Artifact Builder")
    select_language = workflow.start_with(parse_requirements).then(Choice("SelectLanguage"))

    select_language.if_(VariablePath("$.Language") == "python").then(build_python)
    select_language.else_(unknown_language)

    build_python.end()

    return workflow
