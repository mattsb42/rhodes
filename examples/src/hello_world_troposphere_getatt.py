"""
A simple hello-world workflow with a single Lambda Task state.
"""
from troposphere import GetAtt, awslambda

from rhodes.states import StateMachine, Task


def build() -> StateMachine:
    lambda_function = awslambda.Function(
        "HelloWorldFunction", Code=awslambda.Code(ZipFile="foo bar")
    )

    workflow = StateMachine(Comment="A simple minimal example of the States language")

    workflow.start_with(
        Task("Hello World", Resource=GetAtt(lambda_function, "Arn"))
    ).end()

    return workflow
