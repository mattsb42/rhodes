"""
Simple workflow using the Map state.
"""
from rhodes.states import Map, Parameters, StateMachine, Task
from rhodes.structures import ContextPath, JsonPath


def build() -> StateMachine:
    validate_task = Task("Validate", Resource="arn:aws:lambda:us-east-1:123456789012:function:ship-val")

    state_iterator = StateMachine()
    state_iterator.start_with(validate_task).end()

    mapper = Map(
        "ValidateAll",
        InputPath=JsonPath("$.detail"),
        ItemsPath=JsonPath("$.shipped"),
        Parameters=Parameters(Execution=ContextPath().Execution.Id, Payload=JsonPath("$")),
        MaxConcurrency=0,
        Iterator=state_iterator,
        ResultPath=JsonPath("$.detail.shipped"),
    )

    workflow = StateMachine(Comment="Simple state machine with one map state")
    workflow.start_with(mapper).end()

    return workflow
