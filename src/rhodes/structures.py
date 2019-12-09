"""Other structures for Rhodes."""
from typing import Any, Dict, Union

import attr
import jsonpath_rw
from attr.validators import instance_of

from rhodes._serialization import serialize_name_and_value

__all__ = ("JsonPath", "ContextPath", "Parameters")


def _convert_path(value: Union[str, jsonpath_rw.JSONPath, "JsonPath"]) -> jsonpath_rw.JSONPath:
    if isinstance(value, jsonpath_rw.JSONPath):
        return value

    if isinstance(value, JsonPath):
        return value.path

    return jsonpath_rw.parse(value)


@attr.s
class JsonPath:
    """Represents a JSONPath variable in request/response body."""

    path: jsonpath_rw.JSONPath = attr.ib(validator=instance_of(jsonpath_rw.JSONPath), converter=_convert_path)

    def __str__(self):
        return str(self.path)

    def to_dict(self) -> str:
        return str(self)


@attr.s
class ContextPath:
    """Represents a JSONPath(ish) variable in the Context Object.

    https://docs.aws.amazon.com/step-functions/latest/dg/input-output-contextobject.html
    """

    _path: str = attr.ib(default="$$")

    @_path.validator
    def _validate_path(self, attribute, value):
        _valid_paths = {
            "Execution": {"Id": False, "Input": True, "StartTime": False},
            "State": {"EnteredTime": False, "Name": False, "RetryCount": False},
            "StateMachine": {"Id": False},
            "Task": {"Token": False},
            "Map": {"Item": {"Index": False, "Value": False}},
        }

        def _validate_parts(tree, fields):
            # retrieve relative root
            key, *remaining = fields

            # look for valid children
            try:
                inner_tree = tree[key]
            except KeyError:
                raise ValueError("Invalid Context Path")

            if isinstance(inner_tree, dict):
                if not remaining:
                    # Requested path is a sub-object not an individual member
                    return

                return _validate_parts(inner_tree, remaining)

            if not inner_tree and remaining:
                # Requested path is an unknown child
                raise ValueError("Invalid Context Path")

        # TODO: Verify that:
        #  1. Aside from the leading $, path is a valid JSONPath
        #  2. If the prefix is anything other than $$.Execution.Input,
        #   the path must be on the known list.

        parts = value.split(".")

        # Path MUST start with "$$." not "$." to identify as Context Object
        if parts[0] != "$$":
            raise ValueError("Invalid Context Path")

        if len(parts) == 1:
            # Requested path is the entire Context Object
            return

        _validate_parts(_valid_paths, parts[1:])

    def __str__(self):
        return self._path

    def to_dict(self) -> str:
        return str(self)

    def __getattr__(self, item):
        return ContextPath(f"{self._path}.{item}")


class Parameters:
    def __init__(self, **kwargs):
        self._map = kwargs

    def to_dict(self) -> Dict[str, Any]:
        def _inner():
            for name, value in self._map.items():
                new_name, new_value = serialize_name_and_value(name=name, value=value)

                if isinstance(value, JsonPath) or isinstance(value, ContextPath):
                    # If you manually provide path strings, you must manually set the parameter suffix.
                    if not new_name.endswith(".$"):
                        new_name += ".$"

                yield new_name, new_value

        return dict(_inner())

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{name}={value!r}' for name, value in self._map.items())})"
