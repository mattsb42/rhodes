"""Other structures for Rhodes."""
from typing import Union

import attr
import jsonpath_rw
from attr.validators import instance_of

__all__ = ("JsonPath",)


def _convert_path(value: Union[str, jsonpath_rw.JSONPath, "JsonPath"]) -> jsonpath_rw.JSONPath:
    if isinstance(value, jsonpath_rw.JSONPath):
        return value

    if isinstance(value, JsonPath):
        return value.path

    return jsonpath_rw.parse(value)


@attr.s(eq=False, order=False)
class JsonPath:
    """Represents a JSONPath variable in request/response body."""

    path: jsonpath_rw.JSONPath = attr.ib(validator=instance_of(jsonpath_rw.JSONPath), converter=_convert_path)

    def __str__(self):
        return str(self.path)
