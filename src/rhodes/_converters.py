"""Converter functions for use with ``attrs`` attributes."""
from enum import Enum
from typing import Optional, Union

import jsonpath_rw

from .structures import JsonPath

__all__ = ("convert_to_json_path",)


def convert_to_json_path(value: Optional[Union[str, Enum, jsonpath_rw.JSONPath, JsonPath]]) -> Union[None, JsonPath]:
    """Converter for any attributes that must be :class:`JsonPath` instances."""
    if value is None:
        return value

    if isinstance(value, JsonPath):
        return value

    if isinstance(value, Enum):
        value = value.value

    return JsonPath(value)
