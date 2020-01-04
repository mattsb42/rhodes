"""General internal utilities."""
from functools import partial
from typing import Any, Callable, Optional, Type, TypeVar

import attr

from .exceptions import InvalidDefinitionError

__all__ = ("RequiredValue", "require_field", "RHODES_ATTRIB", "docstring_with_param")


@attr.s(auto_attribs=True)
class RequiredValue:
    """Identify a required value and the error message that should be raised if it is missing.

    This is used to identify parameters that are required on serialization
    but not necessarily initialization.
    """

    field_name: str
    error_message: str


def require_field(*, instance: Any, required_value: RequiredValue, validator: Callable[[Any], bool] = bool):
    """Verify that a required field contains a valid value."""
    # TODO: The validator here is incorrect.
    #  I need to pull the validator for the attribute from the instance class.
    if not hasattr(instance, required_value.field_name):
        raise InvalidDefinitionError(f"Field {required_value.field_name!r} missing.")

    if not validator(getattr(instance, required_value.field_name)):
        raise InvalidDefinitionError(required_value.error_message)


RHODES_ATTRIB = partial(attr.ib, default=None, kw_only=True)

TypeMirror = TypeVar("TypeMirror", bound=Type[Any])


NO_DEFAULT = object()


def docstring_with_param(
    cls: TypeMirror,
    variable_name: str,
    variable_type: Optional[Type] = None,
    description: Optional[str] = "",
    default: Optional[Any] = NO_DEFAULT,
) -> str:
    """Create a new docstring for the specified class that now includes a parameter entry for the variable.

    :param cls: Class from which to get docstring
    :param str variable_name: Name of parameter
    :param type variable_type: Parameter type
    :param str description: Description for parameter to add to docstring
    :param default: The default value if this parameter is optional
    """
    base = getattr(cls, "__doc__", "")[:].rstrip("\n")

    base += "\n    :param "

    if variable_type is not None:
        base += f"{variable_type.__name__} "

    base += f"{variable_name}: {description}"

    if default is not NO_DEFAULT:
        base += f" (default: ``{default!r}``)"

    base += "\n"

    return base
