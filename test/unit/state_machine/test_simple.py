"""Simple state machine definition tests."""
import pytest

from rhodes import StateMachine, choice_rules
from rhodes.exceptions import InvalidDefinitionError
from rhodes.states import Choice, Fail, Map, Parallel, Pass, State, Succeed, Task, Wait
from rhodes.structures import Variable

from ..unit_test_helpers import state_machine_body

pytestmark = [pytest.mark.local, pytest.mark.functional]


def test_hello_world():
    expected = state_machine_body("hello-world")

    test = StateMachine(
        Comment="A simple minimal example of the States language",
        StartAt="Hello World",
        States={
            "Hello World": Task(
                "Hello World", Resource="arn:aws:lambda:us-east-1:123456789012:function:HelloWorld", End=True
            )
        },
    )

    actual = test.to_dict()

    assert actual == expected


@pytest.mark.parametrize(
    "kwargs",
    (
        dict(),
        dict(States=[]),
        dict(States={"AlwaysBlue": Succeed("AlwaysBlue")}),
        dict(StartAt="AlwaysBlue"),
        dict(States={"AlwaysBlue": Succeed("AlwaysBlue")}, StartAt="Unknown"),
    ),
)
def test_required_values(kwargs):
    test = StateMachine(**kwargs)

    with pytest.raises(InvalidDefinitionError) as excinfo:
        test.to_dict()


def test_three_tasks():
    expected = state_machine_body("three-tasks")

    test = StateMachine(
        Comment="This is a state machine with three simple tasks.",
        StartAt="TaskOne",
        States=dict(
            TaskOne=Task("TaskOne", Resource="arn:aws:lambda:us-east-1:123456789012:function:One", Next="TaskTwo"),
            TaskTwo=Task("TaskTwo", Resource="arn:aws:lambda:us-east-1:123456789012:function:Two", Next="TaskThree"),
            TaskThree=Task("TaskThree", Resource="arn:aws:lambda:us-east-1:123456789012:function:Three", End=True),
        ),
    )

    actual = test.to_dict()

    assert actual == expected


def test_three_tasks_new_1():
    test = StateMachine(Comment="This is a state machine with three simple tasks.")

    task_one = test.start_with(Task("TaskOne", Resource="arn:aws:lambda:us-east-1:123456789012:function:One"))
    task_two = task_one.then(Task("TaskTwo", Resource="arn:aws:lambda:us-east-1:123456789012:function:Two"))
    task_three = task_two.then(Task("TaskThree", Resource="arn:aws:lambda:us-east-1:123456789012:function:Three"))
    task_three.end()

    expected = state_machine_body("three-tasks")
    actual = test.to_dict()
    assert actual == expected


def test_simple_choice():
    test = StateMachine(
        Comment="This is a simple state machine with a single choice and three end states.",
        StartAt="TheBeginning",
        States=dict(
            TheBeginning=Choice(
                "TheBeginning",
                Choices=[
                    choice_rules.StringEquals(Variable="$.value", Value="A", Next="ResultA"),
                    choice_rules.StringEquals(Variable="$.value", Value="B", Next="ResultB1"),
                ],
                Default="Unknown",
            ),
            ResultA=Task("ResultA", Resource="arn:aws:lambda:us-east-1:123456789012:function:A", End=True),
            ResultB1=Task("ResultB1", Resource="arn:aws:lambda:us-east-1:123456789012:function:B1", Next="ResultB2"),
            ResultB2=Task("ResultB2", Resource="arn:aws:lambda:us-east-1:123456789012:function:B2", End=True),
            Unknown=Fail("Unknown", Error="Unhandled Case", Cause="Unknown Value"),
        ),
    )

    expected = state_machine_body("simple-choice")
    actual = test.to_dict()
    assert actual == expected


def test_simple_choice_new_1():
    test = StateMachine(Comment="This is a simple state machine with a single choice and three end states.")
    result_a = test.add_state(Task("ResultA", Resource="arn:aws:lambda:us-east-1:123456789012:function:A", End=True))
    result_b1 = test.add_state(Task("ResultB1", Resource="arn:aws:lambda:us-east-1:123456789012:function:B1"))
    result_b1.then(Task("ResultB2", Resource="arn:aws:lambda:us-east-1:123456789012:function:B2", End=True))
    unknown = test.add_state(Fail("Unknown", Error="Unhandled Case", Cause="Unknown Value"))

    decision = test.start_with(Choice("TheBeginning"))
    decision.if_(choice_rules.StringEquals(Variable="$.value", Value="A")).then_(result_a)
    decision.if_(choice_rules.StringEquals(Variable="$.value", Value="B")).then_(result_b1)
    decision.else_(unknown)

    expected = state_machine_body("simple-choice")
    actual = test.to_dict()
    assert actual == expected


def test_simple_choice_new_2():
    test = StateMachine(Comment="This is a simple state machine with a single choice and three end states.")
    result_a = test.add_state(Task("ResultA", Resource="arn:aws:lambda:us-east-1:123456789012:function:A", End=True))
    result_b1 = test.add_state(Task("ResultB1", Resource="arn:aws:lambda:us-east-1:123456789012:function:B1"))
    result_b1.then(Task("ResultB2", Resource="arn:aws:lambda:us-east-1:123456789012:function:B2", End=True))
    unknown = test.add_state(Fail("Unknown", Error="Unhandled Case", Cause="Unknown Value"))

    decision = test.start_with(Choice("TheBeginning"))
    decision.if_(Variable("$.value") == "A").then_(result_a)
    decision.if_(Variable("$.value") == "B").then_(result_b1)
    decision.else_(unknown)

    expected = state_machine_body("simple-choice")
    actual = test.to_dict()
    assert actual == expected


def test_simple_choice_new_3():
    test = StateMachine(Comment="This is a simple state machine with a single choice and three end states.")
    result_a = Task("ResultA", Resource="arn:aws:lambda:us-east-1:123456789012:function:A", End=True)
    result_b1 = test.add_state(Task("ResultB1", Resource="arn:aws:lambda:us-east-1:123456789012:function:B1"))
    result_b1.then(Task("ResultB2", Resource="arn:aws:lambda:us-east-1:123456789012:function:B2", End=True))
    unknown = Fail("Unknown", Error="Unhandled Case", Cause="Unknown Value")

    decision = test.start_with(Choice("TheBeginning"))
    decision.if_(Variable("$.value") == "A").then_(result_a)
    decision.if_(Variable("$.value") == "B").then_(result_b1)
    decision.else_(unknown)

    expected = state_machine_body("simple-choice")
    actual = test.to_dict()
    assert actual == expected


def test_simple_choice_new_3_3():
    test = StateMachine(Comment="This is a simple state machine with a single choice and three end states.")
    result_a = Task("ResultA", Resource="arn:aws:lambda:us-east-1:123456789012:function:A").end()
    result_b1 = test.add_state(Task("ResultB1", Resource="arn:aws:lambda:us-east-1:123456789012:function:B1"))
    result_b1.then(Task("ResultB2", Resource="arn:aws:lambda:us-east-1:123456789012:function:B2").end())
    unknown = Fail("Unknown", Error="Unhandled Case", Cause="Unknown Value")

    decision = test.start_with(Choice("TheBeginning"))
    decision.if_(Variable("$.value") == "A").then_(result_a)
    decision.if_(Variable("$.value") == "B").then_(result_b1)
    decision.else_(unknown)

    expected = state_machine_body("simple-choice")
    actual = test.to_dict()
    assert actual == expected


def test_simple_choice_new_4():
    test = StateMachine(Comment="This is a simple state machine with a single choice and three end states.")

    decision = test.start_with(Choice("TheBeginning"))
    decision.if_(Variable("$.value") == "A").then_(
        Task("ResultA", Resource="arn:aws:lambda:us-east-1:123456789012:function:A").end()
    )
    result_b1 = decision.if_(Variable("$.value") == "B").then_(
        Task("ResultB1", Resource="arn:aws:lambda:us-east-1:123456789012:function:B1")
    )
    result_b1.then(Task("ResultB2", Resource="arn:aws:lambda:us-east-1:123456789012:function:B2").end())
    decision.else_(Fail("Unknown", Error="Unhandled Case", Cause="Unknown Value"))

    expected = state_machine_body("simple-choice")
    actual = test.to_dict()
    assert actual == expected


def test_simple_parallel():
    expected = state_machine_body("simple-parallel")

    test = StateMachine(
        Comment="Parallel Example.",
        StartAt="LookupCustomerInfo",
        States=dict(
            LookupCustomerInfo=Parallel(
                "LookupCustomerInfo",
                End=True,
                Branches=[
                    StateMachine(
                        StartAt="LookupAddress",
                        States=dict(
                            LookupAddress=Task(
                                "LookupAddress",
                                Resource="arn:aws:lambda:us-east-1:123456789012:function:AddressFinder",
                                End=True,
                            )
                        ),
                    ),
                    StateMachine(
                        StartAt="LookupPhone",
                        States=dict(
                            LookupPhone=Task(
                                "LookupPhone",
                                Resource="arn:aws:lambda:us-east-1:123456789012:function:PhoneFinder",
                                End=True,
                            )
                        ),
                    ),
                ],
            )
        ),
    )

    actual = test.to_dict()

    assert actual == expected


def test_simple_parallel_new_1():
    lookup_address = StateMachine()
    lookup_address.start_with(
        Task("LookupAddress", Resource="arn:aws:lambda:us-east-1:123456789012:function:AddressFinder")
    ).end()

    lookup_phone = StateMachine()
    lookup_phone.start_with(
        Task("LookupPhone", Resource="arn:aws:lambda:us-east-1:123456789012:function:PhoneFinder")
    ).end()

    test = StateMachine(Comment="Parallel Example.")
    test.start_with(Parallel("LookupCustomerInfo", Branches=[lookup_address, lookup_phone])).end()

    expected = state_machine_body("simple-parallel")
    actual = test.to_dict()
    assert actual == expected


def test_simple_parallel_new_2():
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

    test = StateMachine(Comment="Parallel Example.")
    test.start_with(parallel_run).end()

    expected = state_machine_body("simple-parallel")
    actual = test.to_dict()
    assert actual == expected


def test_simple_map():
    test = StateMachine(
        Comment="Simple state machine with one map state",
        StartAt="ValidateAll",
        States=dict(
            ValidateAll=Map(
                "ValidateAll",
                InputPath="$.detail",
                ItemsPath="$.shipped",
                MaxConcurrency=0,
                Iterator=StateMachine(
                    StartAt="Validate",
                    States=dict(
                        Validate=Task(
                            "Validate", Resource="arn:aws:lambda:us-east-1:123456789012:function:ship-val", End=True
                        )
                    ),
                ),
                ResultPath="$.detail.shipped",
                End=True,
            )
        ),
    )

    expected = state_machine_body("simple-map")
    actual = test.to_dict()
    assert actual == expected


def test_simple_map_new_1():
    validate_task = Task("Validate", Resource="arn:aws:lambda:us-east-1:123456789012:function:ship-val")

    state_iterator = StateMachine()
    state_iterator.start_with(validate_task).end()

    mapper = Map(
        "ValidateAll",
        InputPath="$.detail",
        ItemsPath="$.shipped",
        MaxConcurrency=0,
        Iterator=state_iterator,
        ResultPath="$.detail.shipped",
    )

    test = StateMachine(Comment="Simple state machine with one map state")
    test.start_with(mapper).end()

    expected = state_machine_body("simple-map")
    actual = test.to_dict()
    assert actual == expected
