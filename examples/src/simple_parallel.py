"""
Simple workflow using a Parallel state with two concurrent workflows.
"""
from rhodes.states import Parallel, StateMachine, Task


def build() -> StateMachine:
    lookup_address = StateMachine()
    lookup_address.start_with(
        Task("LookupAddress", Resource="arn:aws:lambda:us-east-1:123456789012:function:AddressFinder")
    ).end()

    lookup_phone = StateMachine()
    lookup_phone.start_with(
        Task("LookupPhone", Resource="arn:aws:lambda:us-east-1:123456789012:function:PhoneFinder")
    ).end()

    parallel_run = Parallel("LookupCustomerInfo")
    parallel_run.add_branch(lookup_address)
    parallel_run.add_branch(lookup_phone)

    workflow = StateMachine(Comment="Parallel Example.")
    workflow.start_with(parallel_run).end()

    return workflow
