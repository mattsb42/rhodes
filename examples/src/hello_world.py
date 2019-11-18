"""
A simple hello-world workflow with a single Lambda Task state.
"""
from rhodes.states import StateMachine, Task


def build() -> StateMachine:
    workflow = StateMachine(Comment="A simple minimal example of the States language")

    workflow.start_with(Task("Hello World", Resource="arn:aws:lambda:us-east-1:123456789012:function:HelloWorld")).end()

    return workflow
