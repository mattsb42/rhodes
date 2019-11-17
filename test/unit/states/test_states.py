"""Undifferentiated unit tests for ``rhodes.states``."""
import pytest

from rhodes.states import Parameters

pytestmark = [pytest.mark.local, pytest.mark.functional]


def test_parameters_repr():
    test = Parameters(a="A", b=3, c=True)

    assert repr(test) == "Parameters(a='A', b=3, c=True)"
