"""Unit tests for ``rhodes.structures``."""
import pytest

from rhodes.structures import ContextPath

pytestmark = [pytest.mark.local, pytest.mark.functional]


_VALID_STATIC_CONTEXT_PATHS = (
    "$$",
    "$$.Execution",
    "$$.Execution.Id",
    "$$.Execution.StartTime",
    "$$.State",
    "$$.State.EnteredTime",
    "$$.State.Name",
    "$$.State.RetryCount",
    "$$.StateMachine",
    "$$.StateMachine.Id",
    "$$.Task",
    "$$.Task.Token",
    "$$.Map",
    "$$.Map.Item",
    "$$.Map.Item.Index",
    "$$.Map.Item.Value",
)
_VALID_CONTEXT_PATHS_WITH_INPUT = _VALID_STATIC_CONTEXT_PATHS + (
    "$$.Execution.Input",
    "$$.Execution.Input.foo",
    "$$.Execution.Input.foo.bar",
    "$$.Execution.Input.foo.bar.baz",
)


@pytest.mark.parametrize("path", _VALID_CONTEXT_PATHS_WITH_INPUT)
def test_contextpath_valid(path):
    ContextPath(path=path)


@pytest.mark.parametrize("path", _VALID_CONTEXT_PATHS_WITH_INPUT)
def test_contextpath_getattr_valid(path):
    expected = ContextPath(path=path)

    names = path.split(".")[1:]

    test = ContextPath()
    for name in names:
        test = getattr(test, name)

    assert test == expected


def test_contextpath_getattr_readable():
    """The real testing is via ``test_contextpath_getattr_valid``.

    This test is just to show a more human-readable form.
    """
    assert ContextPath() == ContextPath("$$")
    assert ContextPath().Execution == ContextPath("$$.Execution")
    assert ContextPath().Map.Item.Index == ContextPath("$$.Map.Item.Index")
    assert ContextPath().Execution.Input.foo.bar.baz == ContextPath("$$.Execution.Input.foo.bar.baz")


@pytest.mark.parametrize(
    "path",
    (pytest.param("", id="empty path"), pytest.param("$.Execution", id="valid child but invalid root"))
    + tuple(pytest.param(val + ".foo", id="valid prefix but invalid child") for val in _VALID_STATIC_CONTEXT_PATHS),
)
def test_contextpath_invalid(path):
    with pytest.raises(ValueError) as excinfo:
        ContextPath(path=path)

    excinfo.match("Invalid Context Path")
