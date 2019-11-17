"""Unit test suite for ``rhodes._converters``."""
from enum import Enum

import jsonpath_rw
import pytest

from rhodes._converters import convert_to_json_path
from rhodes.choice_rules import VariablePath
from rhodes.structures import JsonPath

pytestmark = [pytest.mark.local, pytest.mark.functional]


RAW_PATH = "$.path.to.value"


class MyEnum(Enum):
    MY_PATH = RAW_PATH


@pytest.mark.parametrize(
    "path_value",
    (
        pytest.param(RAW_PATH, id="string"),
        pytest.param(MyEnum.MY_PATH, id="enum"),
        pytest.param(jsonpath_rw.parse(RAW_PATH), id="jsonpath_rw.JSONPath"),
        pytest.param(JsonPath(RAW_PATH), id="JsonPath"),
        pytest.param(VariablePath(RAW_PATH), id="VariablePath"),
    ),
)
def test_convert_to_json_path(path_value):
    expected = JsonPath(RAW_PATH)

    test = convert_to_json_path(path_value)

    assert test.path == expected.path
