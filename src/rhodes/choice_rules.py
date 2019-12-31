from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Type

import attr
from attr.validators import instance_of, optional

from rhodes._util import RHODES_ATTRIB, docstring_with_param
from rhodes.exceptions import InvalidDefinitionError
from rhodes.structures import JsonPath

__all__ = (
    "VariablePath",
    "ChoiceRule",
    "StringEquals",
    "StringGreaterThan",
    "StringGreaterThanEquals",
    "StringLessThan",
    "StringLessThanEquals",
    "NumericEquals",
    "NumericGreaterThan",
    "NumericGreaterThanEquals",
    "NumericLessThan",
    "NumericLessThanEquals",
    "BooleanEquals",
    "TimestampEquals",
    "TimestampGreaterThan",
    "TimestampGreaterThanEquals",
    "TimestampLessThan",
    "TimestampLessThanEquals",
    "And",
    "Or",
    "Not",
    "all_",
    "any_",
)


class VariablePath(JsonPath):
    """:class:`JsonPath` variant with overloading helper methods to generate choice rules."""

    # TODO: Add __and__ and __or__ behaviors?

    def __lt__(self, other: Any) -> Type["ChoiceRule"]:
        return _derive_rule(variable=self, operator="<", value=other)

    def __le__(self, other: Any) -> Type["ChoiceRule"]:
        return _derive_rule(variable=self, operator="<=", value=other)

    def __eq__(self, other: Any) -> Type["ChoiceRule"]:
        return _derive_rule(variable=self, operator="==", value=other)

    def __ne__(self, other: Any) -> "Not":
        inner_rule = _derive_rule(variable=self, operator="==", value=other)
        return Not(Rule=inner_rule)

    def __gt__(self, other: Any) -> Type["ChoiceRule"]:
        return _derive_rule(variable=self, operator=">", value=other)

    def __ge__(self, other: Any) -> Type["ChoiceRule"]:
        return _derive_rule(variable=self, operator=">=", value=other)


def _required_next(instance):
    if instance.Next is None:
        raise InvalidDefinitionError("ChoiceRule missing state transition")


def _require_choice_rule_instance(*, class_name: str, attribute_name: str, value):
    if not isinstance(value, ChoiceRule):
        raise TypeError(f'"{class_name}.{attribute_name}" must be a "ChoiceRule". Received "{type(value)}"')


def _require_no_next(*, class_name: str, attribute_name: str, value):
    if value.Next is not None:
        raise ValueError(f'"{class_name}.{attribute_name}" must not have a "Next" value defined.')


def _single_to_dict(instance, suppress_next=False):
    if not suppress_next:
        _required_next(instance)

    instance_dict = {instance.__class__.__name__: instance._serialized_value(), "Variable": str(instance.Variable)}
    if instance.Next is not None:
        instance_dict["Next"] = instance.Next

    return instance_dict


def _convert_to_variable_path(value) -> VariablePath:
    if isinstance(value, VariablePath):
        return value

    return VariablePath(value)


def _single(cls):
    cls.Variable = RHODES_ATTRIB(validator=instance_of(VariablePath), converter=_convert_to_variable_path)
    cls.__doc__ = docstring_with_param(
        cls, "Variable", VariablePath, description="Path to value in state input that will be evaluated"
    )

    cls.Next = RHODES_ATTRIB(validator=optional(instance_of(str)))
    cls.__doc__ = docstring_with_param(
        cls, "Next", description="The state to which to continue if this rule evaluates as true"
    )

    cls.to_dict = _single_to_dict

    return cls


def _multi_to_dict(instance, suppress_next=False):
    if not suppress_next:
        _required_next(instance)

    # TODO: Validate that no children have a Next value

    return {
        instance.__class__.__name__: [rule.to_dict(suppress_next=True) for rule in instance.Rules],
        "Next": instance.Next,
    }


def _validate_multi_subrules(instance, attribute, value):
    for pos, rule in enumerate(value):
        position_name = f"{attribute.name}[{pos}]"
        _require_choice_rule_instance(class_name=instance.__class__.__name__, attribute_name=position_name, value=rule)
        _require_no_next(class_name=instance.__class__.__name__, attribute_name=position_name, value=rule)


def _multi(cls):
    cls.Rules = RHODES_ATTRIB(validator=_validate_multi_subrules)
    cls.__doc__ = docstring_with_param(
        cls, "Rules", description="One or more :class:`ChoiceRule` to evaluate for this rule"
    )

    cls.Next = RHODES_ATTRIB(validator=optional(instance_of(str)))
    cls.__doc__ = docstring_with_param(
        cls, "Next", description="The state to which to continue if this rule evaluates as true"
    )

    cls.to_dict = _multi_to_dict

    return cls


def _string(cls):
    cls = _single(cls)

    cls.Value = RHODES_ATTRIB(validator=instance_of(str))
    cls.__doc__ = docstring_with_param(cls, "Value", str, description="The value to which to compare ``Variable``")

    return cls


def _number(cls):
    cls = _single(cls)

    def _numeric_converter(value) -> Decimal:
        if isinstance(value, Decimal):
            return value

        return Decimal(str(value))

    def _value_serializer(instance) -> float:
        return float(instance.Value)

    # TODO: Note that for interoperability,
    #  numeric comparisons should not be assumed to work
    #  with values outside the magnitude or precision
    #  representable using the IEEE 754-2008 “binary64” data type.
    #  In particular,
    #  integers outside of the range [-(253)+1, (253)-1]
    #  might fail to compare in the expected way.
    cls.Value = RHODES_ATTRIB(validator=instance_of(Decimal), converter=_numeric_converter)
    cls.__doc__ = docstring_with_param(cls, "Value", description="The value to which to compare ``Variable``")

    cls._serialized_value = _value_serializer

    return cls


def _bool(cls):
    cls = _single(cls)

    cls.Value = RHODES_ATTRIB(validator=instance_of(bool))
    cls.__doc__ = docstring_with_param(cls, "Value", bool, description="The value to which to compare ``Variable``")

    return cls


def _timestamp(cls):
    cls = _single(cls)

    def _datetime_validator(instance, attribute, value):
        if value.tzinfo is None:
            raise ValueError(f"'{attribute.name}' must have a 'tzinfo' value set.")

    def _value_serializer(instance):
        return instance.Value.isoformat()

    cls.Value = RHODES_ATTRIB(validator=[instance_of(datetime), _datetime_validator])
    cls.__doc__ = docstring_with_param(cls, "Value", datetime, description="The value to which to compare ``Variable``")

    cls._serialized_value = _value_serializer

    return cls


@attr.s(eq=False)
class ChoiceRule:
    """"""

    member_of = None

    def to_dict(self):
        raise NotImplementedError()

    def __eq__(self, other: "ChoiceRule") -> bool:
        if not isinstance(other, self.__class__):
            return False

        if self.to_dict() != other.to_dict():
            return False

        if self.member_of != other.member_of:
            return False

        return True

    def __ne__(self, other: "ChoiceRule") -> bool:
        return not self.__eq__(other)

    def _serialized_value(self):
        return self.Value

    def then(self, state):
        if self.Next is not None:
            raise InvalidDefinitionError(f"Choice rule already has a defined target")

        self.member_of.member_of.add_state(state)

        self.Next = state.title

        return state


@attr.s(eq=False)
@_string
class StringEquals(ChoiceRule):
    """"""


@attr.s(eq=False)
@_string
class StringLessThan(ChoiceRule):
    """"""


@attr.s(eq=False)
@_string
class StringGreaterThan(ChoiceRule):
    """"""


@attr.s(eq=False)
@_string
class StringLessThanEquals(ChoiceRule):
    """"""


@attr.s(eq=False)
@_string
class StringGreaterThanEquals(ChoiceRule):
    """"""


@attr.s(eq=False)
@_number
class NumericEquals(ChoiceRule):
    """"""


@attr.s(eq=False)
@_number
class NumericLessThan(ChoiceRule):
    """"""


@attr.s(eq=False)
@_number
class NumericGreaterThan(ChoiceRule):
    """"""


@attr.s(eq=False)
@_number
class NumericLessThanEquals(ChoiceRule):
    """"""


@attr.s(eq=False)
@_number
class NumericGreaterThanEquals(ChoiceRule):
    """"""


@attr.s(eq=False)
@_bool
class BooleanEquals(ChoiceRule):
    """"""


@attr.s(eq=False)
@_timestamp
class TimestampEquals(ChoiceRule):
    """"""


@attr.s(eq=False)
@_timestamp
class TimestampLessThan(ChoiceRule):
    """"""


@attr.s(eq=False)
@_timestamp
class TimestampGreaterThan(ChoiceRule):
    """"""


@attr.s(eq=False)
@_timestamp
class TimestampLessThanEquals(ChoiceRule):
    """"""


@attr.s(eq=False)
@_timestamp
class TimestampGreaterThanEquals(ChoiceRule):
    """"""


@attr.s(eq=False)
@_multi
class And(ChoiceRule):
    """"""


@attr.s(eq=False)
@_multi
class Or(ChoiceRule):
    """"""


@attr.s(eq=False)
class Not(ChoiceRule):
    """
    :param ChoiceRule Rule: Rule that must evaluate as false
    :param Next: The state to which to continue if this rule evaluates as true
    """

    Rule = RHODES_ATTRIB(validator=instance_of(ChoiceRule))
    Next = RHODES_ATTRIB(validator=optional(instance_of(str)))

    @Rule.validator
    def _validate_rule(self, attribute, value):
        _require_choice_rule_instance(class_name=self.__class__.__name__, attribute_name=attribute.name, value=value)
        _require_no_next(class_name=self.__class__.__name__, attribute_name=attribute.name, value=value)

    def to_dict(self, suppress_next=False):
        if not suppress_next:
            _required_next(self)

        inner_rule = self.Rule.to_dict(suppress_next=True)
        instance_dict = dict(Not=inner_rule)

        if self.Next is not None:
            instance_dict["Next"] = self.Next

        return instance_dict


_OPERATORS = {
    "string": {
        "==": StringEquals,
        "<": StringLessThan,
        "<=": StringLessThanEquals,
        ">": StringGreaterThan,
        ">=": StringGreaterThanEquals,
    },
    "number": {
        "==": NumericEquals,
        "<": NumericLessThan,
        "<=": NumericLessThanEquals,
        ">": NumericGreaterThan,
        ">=": NumericGreaterThanEquals,
    },
    "time": {
        "==": TimestampEquals,
        "<": TimestampLessThan,
        "<=": TimestampLessThanEquals,
        ">": TimestampGreaterThan,
        ">=": TimestampGreaterThanEquals,
    },
    "boolean": {"==": BooleanEquals},
}
_TYPE_MAP = {bool: "boolean", int: "number", float: "number", Decimal: "number", str: "string", datetime: "time"}


def _derive_rule(*, variable: VariablePath, operator: str, value) -> Type[ChoiceRule]:
    """Derive the correct :class:`ChoiceRule` based on the specified operator and value.

    :param variable: Path to variable in state data
    :param operator: Desired equality operator string
    :param value: Value to compare against
    """
    if isinstance(value, Enum):
        value = value.value

    try:
        value_type = _TYPE_MAP[type(value)]
    except KeyError:
        raise TypeError(f'Unhandled value type "{type(value)}"')

    try:
        operator_class = _OPERATORS[value_type][operator]
    except KeyError:
        raise ValueError(f'Unhandled operator "{operator}"')

    return operator_class(Variable=variable, Value=value)


def all_(*rules: ChoiceRule) -> And:
    """Helper to assemble several rules into an :class:`And` rule."""
    return And(Rules=list(rules))


def any_(*rules: ChoiceRule) -> Or:
    """Helper to assemble several rules into an :class:`Or` rule."""
    return Or(Rules=list(rules))
