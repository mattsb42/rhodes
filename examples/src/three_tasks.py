"""
Simple workflow with three sequential Lambda Function tasks.
"""
from rhodes.states import StateMachine, Task


def build() -> StateMachine:
    workflow = StateMachine(Comment="This is a state machine with three simple tasks.")

    workflow.start_with(
        Task("TaskOne", Resource="arn:aws:lambda:us-east-1:123456789012:function:One")
    ).then(
        Task("TaskTwo", Resource="arn:aws:lambda:us-east-1:123456789012:function:Two")
    ).then(
        Task(
            "TaskThree", Resource="arn:aws:lambda:us-east-1:123456789012:function:Three"
        )
    ).end()

    return workflow
