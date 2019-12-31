from typing import Any

import attr
from attr.validators import instance_of, optional

from rhodes._converters import convert_to_json_path
from rhodes._util import RHODES_ATTRIB, docstring_with_param
from rhodes.exceptions import InvalidDefinitionError
from rhodes.structures import JsonPath, Parameters

__all__ = ("state", "task_type")


def _next_and_end(cls: "StateMirror") -> "StateMirror":
    """Add "Next" and "End" parameters to the class.
    Also adds the "then()" and "end()" helper methods.
    """

    def _validate_next(instance, attribute: attr.Attribute, value: Any):
        if value is not None and instance.End is not None:
            raise ValueError("Only one of 'Next' and 'End' is allowed")

    cls.Next = RHODES_ATTRIB(validator=(optional(instance_of(str)), _validate_next))
    cls.__doc__ = docstring_with_param(cls, "Next", description="The state that will follow this state")

    def _validate_end(instance, attribute: attr.Attribute, value: Any):
        if value is not None and instance.Next is not None:
            raise ValueError("Only one of 'Next' and 'End' is allowed")

        if value is not None and value is not True:
            raise ValueError("If 'End' is set, value must be True")

    cls.End = RHODES_ATTRIB(validator=(optional(instance_of(bool)), _validate_end))
    cls.__doc__ = docstring_with_param(cls, "End", bool, description="This state is a terminal state")

    def _then(instance, next_state):
        """Set the next state in this state machine."""

        if instance.End:
            raise InvalidDefinitionError(
                "Cannot set state transition." f"State {instance.title!r} already has an end condition."
            )

        instance.member_of.add_state(next_state)
        # TODO: set reference rather than extracting name
        instance.Next = next_state.title
        return next_state

    cls.then = _then

    def _end(instance):
        """Make this state a terminal state."""

        if instance.Next:
            raise InvalidDefinitionError(
                "Cannot set end condition." f"State {instance.title!r} already has a state transition."
            )

        instance.End = True

        return instance

    cls.end = _end

    return cls


def _parameters(cls: "StateMirror") -> "StateMirror":
    """Add the "Parameters" parameter to the class."""
    cls.Parameters = RHODES_ATTRIB(validator=optional(instance_of(Parameters)))
    cls.__doc__ = docstring_with_param(
        cls,
        "Parameters",
        Parameters,
        description="Additional parameters for Step Functions to provide to connected resource",
    )

    return cls


def _result_path(cls: "StateMirror") -> "StateMirror":
    """Add the "ResultPath" parameter to the class."""
    cls.ResultPath = RHODES_ATTRIB(
        default=JsonPath("$"), validator=optional(instance_of(JsonPath)), converter=convert_to_json_path
    )
    cls.__doc__ = docstring_with_param(
        cls,
        "ResultPath",
        JsonPath,
        description="Where in the state input data to place the results of this state",
        default=JsonPath("$"),
    )

    return cls


def _catch_retry(cls: "StateMirror") -> "StateMirror":
    """Add the "Catch" and "Retry" parameters to the class."""
    cls.Retry = RHODES_ATTRIB()
    cls.__doc__ = docstring_with_param(cls, "Retry")

    cls.Catch = RHODES_ATTRIB()
    cls.__doc__ = docstring_with_param(cls, "Catch")

    return cls


def _input_output(cls: "StateMirror") -> "StateMirror":
    """Add the "InputPath" and "OutputPath" parameters to the class."""

    cls.InputPath = RHODES_ATTRIB(
        default=JsonPath("$"), validator=optional(instance_of(JsonPath)), converter=convert_to_json_path
    )
    cls.__doc__ = docstring_with_param(
        cls,
        "InputPath",
        JsonPath,
        description="The portion of the state input data to be used as input for the state",
        default=JsonPath("$"),
    )

    cls.OutputPath = RHODES_ATTRIB(
        default=JsonPath("$"), validator=optional(instance_of(JsonPath)), converter=convert_to_json_path
    )
    cls.__doc__ = docstring_with_param(
        cls,
        "OutputPath",
        JsonPath,
        description="The portion of the state input data to be passed to the next state",
        default=JsonPath("$"),
    )

    return cls


def task_type(cls: "StateMirror") -> "StateMirror":
    """Add common parameters used by all "Task" types."""

    cls = state(cls)
    cls = _next_and_end(cls)
    cls = _input_output(cls)
    cls = _result_path(cls)
    cls = _catch_retry(cls)

    def _validate_positive_value(instance, attribute: attr.Attribute, value: int):
        if value is not None and not value > 0:
            raise ValueError(f"{instance.__class__.__name__} parameter '{attribute.name}' value must be positive")

    # default=99999999
    cls.TimeoutSeconds = RHODES_ATTRIB(validator=(optional(instance_of(int)), _validate_positive_value))
    cls.__doc__ = docstring_with_param(
        cls, "TimeoutSeconds", int, description="Maximum time that this state is allowed to run"
    )

    cls.HeartbeatSeconds = RHODES_ATTRIB(validator=(optional(instance_of(int)), _validate_positive_value))
    cls.__doc__ = docstring_with_param(
        cls, "HeartbeatSeconds", int, description="Maximum time allowed between heartbeat responses from state"
    )

    return cls


def state(cls: "StateMirror") -> "StateMirror":
    """Add common parameters used by all states."""

    cls.__doc__ = docstring_with_param(cls, "title", str, description="Name of state in state machine")

    cls.__doc__ = docstring_with_param(
        cls, "Comment", str, description="Human-readable description of the state", default=""
    )

    return cls
