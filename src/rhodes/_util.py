"""Utilities for use in Rhodes."""
from functools import partial
from typing import Any, Callable

import attr

from .exceptions import InvalidDefinitionError

__all__ = ("RequiredValue", "require_field", "RHODES_ATTRIB")


@attr.s(auto_attribs=True)
class RequiredValue:
    field_name: str
    error_message: str


def require_field(*, instance: Any, required_value: RequiredValue, validator: Callable[[Any], bool] = bool):
    # TODO: The validator here is incorrect.
    #  I need to pull the validatidator for the attribute from the instance class.
    if not hasattr(instance, required_value.field_name):
        raise InvalidDefinitionError(f"Field {required_value.field_name!r} missing.")

    if not validator(getattr(instance, required_value.field_name)):
        raise InvalidDefinitionError(required_value.error_message)


RHODES_ATTRIB = partial(attr.ib, default=None, kw_only=True)
