"""Unit tests for ``rhodes.choice_rules``."""
import operator
from datetime import datetime
from decimal import Decimal
from functools import partial

import pytest
import pytz

from rhodes.choice_rules import (
    And,
    BooleanEquals,
    ChoiceRule,
    Not,
    NumericEquals,
    NumericGreaterThan,
    NumericGreaterThanEquals,
    NumericLessThan,
    NumericLessThanEquals,
    Or,
    StringEquals,
    StringGreaterThan,
    StringGreaterThanEquals,
    StringLessThan,
    StringLessThanEquals,
    TimestampEquals,
    TimestampGreaterThan,
    TimestampGreaterThanEquals,
    TimestampLessThan,
    TimestampLessThanEquals,
    all_,
    any_,
)
from rhodes.structures import Variable

from ..unit_test_helpers import choice_rule_body, load_and_test_vectors

pytestmark = [pytest.mark.local, pytest.mark.functional]
_load_and_test_vector = partial(load_and_test_vectors, choice_rule_body)

_OPERATOR_MAP = dict(
    GreaterThan=operator.gt,
    GreaterThanEquals=operator.ge,
    LessThan=operator.lt,
    LessThanEquals=operator.le,
    Equals=operator.eq,
)


@pytest.mark.parametrize("name, override_kwargs", (("CheckTrue", dict(Value=True)), ("CheckFalse", dict(Value=False))))
def test_boolean_good(name, override_kwargs):
    kwargs = dict(Next="NextState", Variable="$.value")
    kwargs.update(override_kwargs)

    test = BooleanEquals(**kwargs)

    _load_and_test_vector(kind="boolean", name=name, value=test)


def _timestamp_values():
    for cls in (
        TimestampEquals,
        TimestampGreaterThan,
        TimestampGreaterThanEquals,
        TimestampLessThan,
        TimestampLessThanEquals,
    ):
        base_name = cls.__name__.replace("Timestamp", "")
        yield (f"{base_name}Date", cls, dict(Value=pytz.utc.localize(datetime(2016, 12, 1))))
        yield (
            f"{base_name}DateTime",
            cls,
            dict(Value=pytz.timezone("US/Pacific").localize(datetime(2016, 12, 1, 15, 7, 7))),
        )


@pytest.mark.parametrize("name, cls, override_kwargs", _timestamp_values())
def test_timestamp_good(name, cls, override_kwargs):
    kwargs = dict(Next="NextState", Variable="$.value")
    kwargs.update(override_kwargs)

    test = cls(**kwargs)

    _load_and_test_vector(kind="timestamp", name=name, value=test)


def _timestamp_variable_statements():
    for name, cls, override_kwargs in _timestamp_values():
        base_name = cls.__name__.replace("Timestamp", "")
        yield (name, _OPERATOR_MAP[base_name], override_kwargs["Value"])


@pytest.mark.parametrize("name, op, value", _timestamp_variable_statements())
def test_timestamp_good_with_variable(name, op, value):
    test = op(Variable("$.value"), value)
    # TODO: Change this to use ChoiceRule.then_() once they can exist outside of a parent
    test.Next = "NextState"

    _load_and_test_vector(kind="timestamp", name=name, value=test)


@pytest.mark.parametrize(
    "override_kwargs",
    (
        pytest.param(dict(Value="2016-12-01"), id="date string"),
        pytest.param(dict(Value=datetime(2016, 12, 1)), id="timezone-naive datetime"),
    ),
)
@pytest.mark.parametrize(
    "cls",
    (TimestampEquals, TimestampGreaterThan, TimestampGreaterThanEquals, TimestampLessThan, TimestampLessThanEquals),
)
def test_timestamp_invalid(cls, override_kwargs):
    kwargs = dict(Next="NextState", Variable="$.value")
    kwargs.update(override_kwargs)

    with pytest.raises(Exception):
        cls(**kwargs)


@pytest.mark.parametrize(
    "name, cls, override_kwargs",
    (
        ("Equals", StringEquals, dict(Value="Lorem ipsum dolor sit amet")),
        ("GreaterThan", StringGreaterThan, dict(Value="Lorem ipsum dolor sit amet")),
        ("GreaterThanEquals", StringGreaterThanEquals, dict(Value="Lorem ipsum dolor sit amet")),
        ("LessThan", StringLessThan, dict(Value="Lorem ipsum dolor sit amet")),
        ("LessThanEquals", StringLessThanEquals, dict(Value="Lorem ipsum dolor sit amet")),
    ),
)
def test_string_good(name, cls, override_kwargs):
    kwargs = dict(Next="NextState", Variable="$.value")
    kwargs.update(override_kwargs)

    test = cls(**kwargs)

    _load_and_test_vector(kind="string", name=name, value=test)


@pytest.mark.parametrize("override_kwargs", (dict(Value=42),))
@pytest.mark.parametrize(
    "cls", (StringEquals, StringGreaterThan, StringGreaterThanEquals, StringLessThan, StringLessThanEquals)
)
def test_string_invalid(cls, override_kwargs):
    kwargs = dict(Next="NextState", Variable="$.value")
    kwargs.update(override_kwargs)

    with pytest.raises(Exception):
        cls(**kwargs)


def _numeric_values():
    for cls in (NumericEquals, NumericLessThan, NumericLessThanEquals, NumericGreaterThan, NumericGreaterThanEquals):
        base_name = cls.__name__.replace("Numeric", "")
        for value in (42, 42.0, "42", "42.0", Decimal("42"), Decimal("42.0")):
            yield (base_name, cls, dict(Value=value))


@pytest.mark.parametrize("name, cls, override_kwargs", _numeric_values())
def test_numeric_good(name, cls, override_kwargs):
    kwargs = dict(Next="NextState", Variable="$.value")
    kwargs.update(override_kwargs)

    test = cls(**kwargs)

    _load_and_test_vector(kind="numeric", name=name, value=test)


@pytest.mark.parametrize("override_kwargs", (dict(Value="Lorem ipsum dolor sit amet"),))
@pytest.mark.parametrize(
    "cls", (NumericEquals, NumericGreaterThan, NumericGreaterThanEquals, NumericLessThan, NumericLessThanEquals)
)
def test_numeric_invalid(cls, override_kwargs):
    kwargs = dict(Next="NextState", Variable="$.value")
    kwargs.update(override_kwargs)

    with pytest.raises(Exception):
        cls(**kwargs)


def test_not_rule_good():
    test = Not(Rule=StringEquals(Variable="$.value", Value="Lorem ipsum dolor sit amet"), Next="NextState")

    _load_and_test_vector(kind="not", name="Simple", value=test)


def test_not_rule_good_with_variable():
    var = Variable("$.value")
    test = var != "Lorem ipsum dolor sit amet"
    # TODO: Change this to use ChoiceRule.then_() once they can exist outside of a parent
    test.Next = "NextState"

    _load_and_test_vector(kind="not", name="Simple", value=test)


def test_and_rule_good():
    test = And(
        Rules=[NumericLessThan(Variable="$.value", Value=30), NumericGreaterThan(Variable="$.value", Value=20)],
        Next="NextState",
    )

    _load_and_test_vector(kind="and", name="Simple", value=test)


def test_and_rule_good_with_variable():
    var = Variable("$.value")
    test = And(Rules=[var < 30, var > 20])
    # TODO: Change this to use ChoiceRule.then_() once they can exist outside of a parent
    test.Next = "NextState"

    _load_and_test_vector(kind="and", name="Simple", value=test)


def test_and_rule_good_with_variable_1():
    var = Variable("$.value")
    test = all_(var < 30, var > 20)
    # TODO: Change this to use ChoiceRule.then_() once they can exist outside of a parent
    test.Next = "NextState"

    _load_and_test_vector(kind="and", name="Simple", value=test)


def test_and_many_rule_good_with_variable_1():
    var = Variable("$.value")
    test = all_(var < 30, var > 20, var != 22, var != 27)
    # TODO: Change this to use ChoiceRule.then_() once they can exist outside of a parent
    test.Next = "NextState"

    _load_and_test_vector(kind="and", name="Many", value=test)


def test_or_rule_good():
    test = Or(
        Rules=[NumericLessThan(Variable="$.value", Value=20), NumericGreaterThan(Variable="$.value", Value=30)],
        Next="NextState",
    )

    _load_and_test_vector(kind="or", name="Simple", value=test)


def test_or_rule_good_with_variable():
    var = Variable("$.value")

    test = Or(Rules=[var < 20, var > 30])
    # TODO: Change this to use ChoiceRule.then_() once they can exist outside of a parent
    test.Next = "NextState"

    _load_and_test_vector(kind="or", name="Simple", value=test)


def test_or_rule_good_with_variable_1():
    var = Variable("$.value")

    test = any_(var < 20, var > 30)
    # TODO: Change this to use ChoiceRule.then_() once they can exist outside of a parent
    test.Next = "NextState"

    _load_and_test_vector(kind="or", name="Simple", value=test)


def test_or_many_rule_good_with_variable_1():
    var = Variable("$.value")

    test = any_(var < 20, var > 30, var == 22, var == 27)
    # TODO: Change this to use ChoiceRule.then_() once they can exist outside of a parent
    test.Next = "NextState"

    _load_and_test_vector(kind="or", name="Many", value=test)
