"""Unit test suite for ``rhodes.states``."""
import pytest

from rhodes.states import Pass

pytestmark = [pytest.mark.local, pytest.mark.functional]


def test_next_or_end():
    with pytest.raises(ValueError) as excinfo:
        Pass("Foo", Next="Bar", End=True)

    excinfo.match("Only one of 'Next' and 'End' is allowed")


def test_invalid_end():
    with pytest.raises(ValueError) as excinfo:
        Pass("Foo", End=False)

    excinfo.match("If 'End' is set, value must be True")
