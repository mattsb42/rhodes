from enum import Enum
from typing import Any, Tuple

try:
    from troposphere import awslambda, stepfunctions, Ref, GetAtt

    TROPOSPHERE = True
except ImportError:
    TROPOSPHERE = False

__all__ = ("serialize_name_and_value",)


def _getatt_arn(value: str) -> str:
    return f"${{{value}.Arn}}"


def _ref(value: str) -> str:
    return f"${{{value}}}"


def _serialize_troposphere_value(value):
    # Inject appropriate Ref/GetAtt for Troposphere
    GET_ARN = (awslambda.Function,)
    GET_REF = (stepfunctions.Activity,)

    if isinstance(value, GET_ARN):
        return _getatt_arn(value.title)

    if isinstance(value, GET_REF):
        return _ref(value.title)

    if isinstance(value, Ref):
        return _ref(value.data["Ref"])

    if isinstance(value, GetAtt):
        return _getatt_arn(value.data["Fn::GetAtt"][0])

    return value


def serialize_name_and_value(*, name: str, value: Any) -> Tuple[str, Any]:
    if TROPOSPHERE:
        value = _serialize_troposphere_value(value)

    if hasattr(value, "to_dict") and callable(value.to_dict):
        return name, value.to_dict()

    if isinstance(value, Enum):
        return name, value.value

    return name, value
