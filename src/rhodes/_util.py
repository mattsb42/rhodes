"""Utilities for use in Rhodes."""
from typing import Any, Callable

import attr

from .exceptions import InvalidDefinitionError


@attr.s(auto_attribs=True)
class RequiredValue:
    field_name: str
    error_message: str


def require_field(*, instance: Any, required_value: RequiredValue, validator: Callable[[Any], bool] = bool):
    if not hasattr(instance, required_value.field_name):
        raise InvalidDefinitionError(f"Field {required_value.field_name!r} missing.")

    if not validator(getattr(instance, required_value.field_name)):
        raise InvalidDefinitionError(required_value.error_message)
