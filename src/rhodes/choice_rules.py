from datetime import datetime
from decimal import Decimal

import attr
from attr.validators import deep_iterable, instance_of, optional

from .exceptions import InvalidDefinitionError


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

    instance_dict = {instance.__class__.__name__: instance._serialized_value(), "Variable": instance.Variable}
    if instance.Next is not None:
        instance_dict["Next"] = instance.Next

    return instance_dict


def _single(cls):
    cls.Variable = attr.ib(validator=instance_of(str))
    cls.Next = attr.ib(default=None, validator=optional(instance_of(str)))
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
    cls.Rules = attr.ib(validator=_validate_multi_subrules)
    cls.Next = attr.ib(default=None, validator=optional(instance_of(str)))
    cls.to_dict = _multi_to_dict

    return cls


def _string(cls):
    cls.Value = attr.ib(validator=instance_of(str))
    cls = _single(cls)

    return cls


def _number(cls):
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
    cls.Value = attr.ib(validator=instance_of(Decimal), converter=_numeric_converter)
    cls._serialized_value = _value_serializer
    cls = _single(cls)

    return cls


def _bool(cls):
    cls.Value = attr.ib(validator=instance_of(bool))
    cls = _single(cls)

    return cls


def _timestamp(cls):
    def _datetime_validator(instance, attribute, value):
        if value.tzinfo is None:
            raise ValueError(f"'{attribute.name}' must have a 'tzinfo' value set.")

    def _value_serializer(instance):
        return instance.Value.isoformat()

    cls.Value = attr.ib(validator=[instance_of(datetime), _datetime_validator])
    cls._serialized_value = _value_serializer
    cls = _single(cls)

    return cls


@attr.s(eq=False)
class ChoiceRule:

    member_of = None

    def __eq__(self, other: "ChoiceRule") -> bool:
        if not isinstance(other, self.__class__):
            return False

        if not self.to_dict() == other.to_dict():
            return False

        if self.member_of != other.member_of:
            return False

        return True

    def __ne__(self, other: "ChoiceRule") -> bool:
        return not self.__eq__(other)

    def _serialized_value(self):
        return self.Value

    def then_(self, state):
        if self.Next is not None:
            raise InvalidDefinitionError(f"Choice rule already has a defined target")

        self.member_of.member_of.add_state(state)

        self.Next = state.name

        return state


@attr.s(eq=False)
@_string
class StringEquals(ChoiceRule):
    pass


@attr.s(eq=False)
@_string
class StringLessThan(ChoiceRule):
    pass


@attr.s(eq=False)
@_string
class StringGreaterThan(ChoiceRule):
    pass


@attr.s(eq=False)
@_string
class StringLessThanEquals(ChoiceRule):
    pass


@attr.s(eq=False)
@_string
class StringGreaterThanEquals(ChoiceRule):
    pass


@attr.s(eq=False)
@_number
class NumericEquals(ChoiceRule):
    pass


@attr.s(eq=False)
@_number
class NumericLessThan(ChoiceRule):
    pass


@attr.s(eq=False)
@_number
class NumericGreaterThan(ChoiceRule):
    pass


@attr.s(eq=False)
@_number
class NumericLessThanEquals(ChoiceRule):
    pass


@attr.s(eq=False)
@_number
class NumericGreaterThanEquals(ChoiceRule):
    pass


@attr.s(eq=False)
@_bool
class BooleanEquals(ChoiceRule):
    pass


@attr.s(eq=False)
@_timestamp
class TimestampEquals(ChoiceRule):
    pass


@attr.s(eq=False)
@_timestamp
class TimestampLessThan(ChoiceRule):
    pass


@attr.s(eq=False)
@_timestamp
class TimestampGreaterThan(ChoiceRule):
    pass


@attr.s(eq=False)
@_timestamp
class TimestampLessThanEquals(ChoiceRule):
    pass


@attr.s(eq=False)
@_timestamp
class TimestampGreaterThanEquals(ChoiceRule):
    pass


@attr.s(eq=False)
@_multi
class And(ChoiceRule):
    pass


@attr.s(eq=False)
@_multi
class Or(ChoiceRule):
    pass


@attr.s(eq=False)
class Not(ChoiceRule):
    Rule = attr.ib(validator=instance_of(ChoiceRule))
    Next = attr.ib(default=None, validator=optional(instance_of(str)))

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


def derive_rule(*, variable: str, operator: str, value) -> ChoiceRule:
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
    return And(Rules=list(rules))


def any_(*rules: ChoiceRule) -> Or:
    return Or(Rules=list(rules))
