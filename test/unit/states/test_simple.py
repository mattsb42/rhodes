"""Unit tests for ``rhodes.states``."""
from datetime import datetime
from functools import partial
from typing import Dict

import pytest
import pytz

from rhodes import StateMachine, choice_rules
from rhodes.states import Choice, Fail, Map, Parallel, Pass, State, Succeed, Task, Wait

from ..unit_test_helpers import load_and_test_vectors, state_body

pytestmark = [pytest.mark.local, pytest.mark.functional]
_load_and_test_vector = partial(load_and_test_vectors, state_body)


def test_pass():
    name = "No-op"
    test = Pass(name, Result={"x-datum": 0.381018, "y-datum": 622.2269926397355}, ResultPath="$.coords", Next="End")

    _load_and_test_vector(kind="pass", name=name, value=test)


def test_task():
    name = "TaskState"
    test = Task(
        name,
        Comment="Task State example",
        Resource="arn:aws:states:us-east-1:123456789012:task:HelloWorld",
        TimeoutSeconds=300,
        HeartbeatSeconds=60,
        Next="NextState",
    )

    _load_and_test_vector(kind="task", name=name, value=test)


def test_choice():
    name = "ChoiceStateX"
    test = Choice(
        name,
        Choices=[
            choice_rules.Not(Rule=choice_rules.StringEquals(Variable="$.type", Value="Private"), Next="Public"),
            choice_rules.And(
                Rules=[
                    choice_rules.NumericGreaterThanEquals(Variable="$.value", Value=20),
                    choice_rules.NumericLessThan(Variable="$.value", Value=30),
                ],
                Next="ValueInTwenties",
            ),
            choice_rules.BooleanEquals(Variable="$.value", Value=True, Next="TrueState"),
            choice_rules.TimestampLessThan(
                Variable="$.value", Value=pytz.utc.localize(datetime(1999, 9, 13, 13, 0, 21)), Next="PartyTime"
            ),
        ],
        Default="DefaultState",
    )

    _load_and_test_vector(kind="choice", name=name, value=test)


@pytest.mark.parametrize(
    "name,kwargs",
    (
        ("wait_ten_seconds", dict(Seconds=10, Next="NextState")),
        ("wait_for_seconds_path", dict(SecondsPath="$.seconds", Next="NextState")),
        ("wait_until_timestamp", dict(Timestamp="2016-03-14T01:59:00Z", Next="NextState")),
        ("wait_until_timestamp_path", dict(TimestampPath="$.expirydate", Next="NextState")),
    ),
)
def test_wait(name: str, kwargs: Dict):
    test = Wait(name, **kwargs)

    _load_and_test_vector(kind="wait", name=name, value=test)


def test_succeed():
    name = "SuccessState"
    test = Succeed(name)

    _load_and_test_vector(kind="succeed", name=name, value=test)


def test_fail():
    name = "FailState"
    test = Fail(name, Error="ErrorA", Cause="Kaiju attack")

    _load_and_test_vector(kind="fail", name=name, value=test)


def test_parallel():
    name = "FunWithMath"
    test = Parallel(
        name,
        Branches=[
            StateMachine(StartAt="Add", States={"Add": Task("Add", Resource="arn:aws:states:::task:Add", End=True)}),
            StateMachine(
                StartAt="Subtract",
                States={"Subtract": Task("Subtract", Resource="arn:aws:states:::task:Subtract", End=True)},
            ),
        ],
        Next="NextState",
    )

    _load_and_test_vector(kind="parallel", name=name, value=test)


def test_parallel_new_1():
    name = "FunWithMath"

    branch_1 = StateMachine()
    branch_1.start_with(Task("Add", Resource="arn:aws:states:::task:Add")).end()
    branch_2 = StateMachine()
    branch_2.start_with(Task("Subtract", Resource="arn:aws:states:::task:Subtract")).end()

    test = Parallel(name)
    test.add_branch(branch_1)
    test.add_branch(branch_2)
    test.Next = "NextState"

    _load_and_test_vector(kind="parallel", name=name, value=test)


def test_map():
    name = "Validate-All"
    test = Map(
        name,
        InputPath="$.detail",
        ItemsPath="$.shipped",
        MaxConcurrency=0,
        Iterator=StateMachine(
            StartAt="Validate",
            States={
                "Validate": Task(
                    "Validate", Resource="arn:aws:lambda:us-east-1:123456789012:function:ship-val", End=True
                )
            },
        ),
        ResultPath="$.detail.shipped",
        End=True,
    )

    _load_and_test_vector(kind="map", name=name, value=test)
