"""
Simple workflow using a choice with three possible branches.
"""
from rhodes.choice_rules import VariablePath
from rhodes.states import Choice, Fail, StateMachine, Task


def build() -> StateMachine:
    workflow = StateMachine(Comment="This is a simple state machine with a single choice and three end states.")

    decision = workflow.start_with(Choice("TheBeginning"))
    decision.if_(VariablePath("$.value") == "A").then(
        Task("ResultA", Resource="arn:aws:lambda:us-east-1:123456789012:function:A").end()
    )
    result_b1 = decision.if_(VariablePath("$.value") == "B").then(
        Task("ResultB1", Resource="arn:aws:lambda:us-east-1:123456789012:function:B1")
    )
    result_b1.then(Task("ResultB2", Resource="arn:aws:lambda:us-east-1:123456789012:function:B2").end())
    decision.else_(Fail("Unknown", Error="Unhandled Case", Cause="Unknown Value"))

    return workflow
