"""Custom attrs validators."""


def _validate_service_integrations(service_name, api_name):
    # type: (str, str) -> bool
    # TODO: Actually do this.
    return True


def is_valid_arn(value):
    # type: (str) -> bool
    try:
        arn_literal, _partition, service, _region, _account, resource_type, name = value.split(":", 6)
    except ValueError:
        return False

    return _validate_service_integrations(service_name=resource_type, api_name=name)


def is_valid_timestamp(value):
    # type: (str) -> bool
    # TODO: Actually do this.
    return True


_CHOICE_COMPARISON_OPERATORS = (
    "StringEquals",
    "StringLessThan",
    "StringGreaterThan",
    "StringLessThanEquals",
    "StringGreaterThanEquals",
    "NumericEquals",
    "NumericLessThan",
    "NumericGreaterThan",
    "NumericLessThanEquals",
    "NumericGreaterThanEquals",
    "BooleanEquals",
    "TimestampEquals",
    "TimestampLessThan",
    "TimestampGreaterThan",
    "TimestampLessThanEquals",
    "TimestampGreaterThanEquals",
    "And",
    "Or",
    "Not",
)
