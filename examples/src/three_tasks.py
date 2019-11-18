"""
Simple workflow with three sequential Lambda Function tasks.
"""
from rhodes.states import StateMachine, Task


def build() -> StateMachine:
    workflow = StateMachine(Comment="This is a state machine with three simple tasks.")

    task_one = workflow.start_with(Task("TaskOne", Resource="arn:aws:lambda:us-east-1:123456789012:function:One"))
    task_two = task_one.then(Task("TaskTwo", Resource="arn:aws:lambda:us-east-1:123456789012:function:Two"))
    task_three = task_two.then(Task("TaskThree", Resource="arn:aws:lambda:us-east-1:123456789012:function:Three"))
    task_three.end()

    return workflow
