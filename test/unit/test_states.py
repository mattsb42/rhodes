"""Unit test suite for ``rhodes.states``."""
import jsonpath_rw
import pytest

from rhodes.states import Pass, StateMachine
from rhodes.structures import JsonPath

pytestmark = [pytest.mark.local, pytest.mark.functional]


def test_next_or_end():
    with pytest.raises(ValueError) as excinfo:
        Pass("Foo", Next="Bar", End=True)

    excinfo.match("Only one of 'Next' and 'End' is allowed")


def test_invalid_end():
    with pytest.raises(ValueError) as excinfo:
        Pass("Foo", End=False)

    excinfo.match("If 'End' is set, value must be True")


@pytest.mark.parametrize(
    "cls, name, value",
    ((Pass, "InputPath", JsonPath("$")), (Pass, "OutputPath", JsonPath("$")), (Pass, "ResultPath", JsonPath("$"))),
)
def test_default_value(cls, name, value):
    instance = cls("Foo")

    test = getattr(instance, name)

    assert test == value


@pytest.mark.parametrize(
    "source_result, requested_promotion, expected_input",
    (("$.foo.bar", "@.baz", "$.foo.bar.baz"), ("$", "@.bar.baz", "$.bar.baz")),
)
@pytest.mark.parametrize("path_reader", (lambda x: x, jsonpath_rw.parse, JsonPath))
def test_promote(path_reader, source_result, requested_promotion, expected_input):
    machine = StateMachine()
    starter = machine.start_with(Pass("Foo", ResultPath=JsonPath(source_result)))
    test = starter.promote(path_reader(requested_promotion))

    assert test.title == "Foo-PromoteResult"
    assert test.InputPath == JsonPath(expected_input)
    assert test.ResultPath == JsonPath(source_result)
    assert test.member_of is machine
