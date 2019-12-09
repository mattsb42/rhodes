from typing import Any

import attr
from attr.validators import instance_of, optional

from rhodes._converters import convert_to_json_path
from rhodes._util import RHODES_ATTRIB
from rhodes.exceptions import InvalidDefinitionError
from rhodes.structures import JsonPath, Parameters


def _next_and_end(cls):
    """Add "Next" and "End" parameters to the class.
    Also adds the "then()" and "end()" helper methods.
    """

    def _validate_next(instance, attribute: attr.Attribute, value: Any):
        if value is not None and instance.End is not None:
            raise ValueError("Only one of 'Next' and 'End' is allowed")

    cls.Next = RHODES_ATTRIB(validator=(optional(instance_of(str)), _validate_next))

    def _validate_end(instance, attribute: attr.Attribute, value: Any):
        if value is not None and instance.Next is not None:
            raise ValueError("Only one of 'Next' and 'End' is allowed")

        if value is not None and value is not True:
            raise ValueError("If 'End' is set, value must be True")

    cls.End = RHODES_ATTRIB(validator=(optional(instance_of(bool)), _validate_end))

    def _then(instance, next_state):
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
        if instance.Next:
            raise InvalidDefinitionError(
                "Cannot set end condition." f"State {instance.title!r} already has a state transition."
            )

        instance.End = True

        return instance

    cls.end = _end

    return cls


def _parameters(cls):
    """Add the "Parameters" parameter to the class."""
    cls.Parameters = RHODES_ATTRIB(validator=optional(instance_of(Parameters)))

    return cls


def _result_path(cls):
    """Add the "ResultPath" parameter to the class."""
    cls.ResultPath = RHODES_ATTRIB(
        default=JsonPath("$"), validator=optional(instance_of(JsonPath)), converter=convert_to_json_path
    )

    return cls


def _catch_retry(cls):
    """Add the "Catch" and "Retry" parameters to the class."""
    cls.Retry = RHODES_ATTRIB()
    cls.Catch = RHODES_ATTRIB()

    return cls


def _input_output(cls):
    """Add the "InputPath" and "OutputPath" parameters to the class."""

    cls.InputPath = RHODES_ATTRIB(
        default=JsonPath("$"), validator=optional(instance_of(JsonPath)), converter=convert_to_json_path
    )
    cls.OutputPath = RHODES_ATTRIB(
        default=JsonPath("$"), validator=optional(instance_of(JsonPath)), converter=convert_to_json_path
    )

    return cls


def task_type(cls):
    """Add common parameters used by all "Task" types."""

    cls = _next_and_end(cls)
    cls = _input_output(cls)
    cls = _result_path(cls)
    cls = _catch_retry(cls)

    def _validate_positive_value(instance, attribute: attr.Attribute, value: int):
        if value is not None and not value > 0:
            raise ValueError(f"{instance.__class__.__name__} parameter '{attribute.name}' value must be positive")

    cls.TimeoutSeconds = RHODES_ATTRIB(validator=(optional(instance_of(int)), _validate_positive_value))
    cls.HeartbeatSeconds = RHODES_ATTRIB(validator=(optional(instance_of(int)), _validate_positive_value))

    return cls
