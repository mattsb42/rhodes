from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Iterable, Optional, Type, Union, overload

import jsonpath_rw

from rhodes._types import StateMirror
from rhodes.states import Choice
from rhodes.structures import JsonPath

class VariablePath(JsonPath):
    def __lt__(self, other: Any) -> Type["ChoiceRule"]: ...
    def __le__(self, other: Any) -> Type["ChoiceRule"]: ...
    def __eq__(self, other: Any) -> Type["ChoiceRule"]: ...  # type: ignore
    def __ne__(self, other: Any) -> Not: ...  # type: ignore
    def __gt__(self, other: Any) -> Type["ChoiceRule"]: ...
    def __ge__(self, other: Any) -> Type["ChoiceRule"]: ...
    # TODO: Figure out how to make this work right
    # @overload
    # def __lt__(self, other: Union[int, float, Decimal]) -> NumericLessThan: ...
    #
    # @overload
    # def __lt__(self, other: str) -> StringLessThan: ...
    #
    # @overload
    # def __lt__(self, other: datetime) -> TimestampLessThan: ...
    #
    # @overload
    # def __le__(self, other: Union[int, float, Decimal]) -> NumericLessThanEquals: ...
    #
    # @overload
    # def __le__(self, other: str) -> StringLessThanEquals: ...
    #
    # @overload
    # def __le__(self, other: datetime) -> TimestampLessThanEquals: ...
    #
    # @overload
    # def __eq__(self, other: Union[int, float, Decimal]) -> NumericEquals: ...
    #
    # @overload
    # def __eq__(self, other: str) -> StringEquals: ...
    #
    # @overload
    # def __eq__(self, other: datetime) -> TimestampEquals: ...
    #
    # @overload
    # def __eq__(self, other: bool) -> BooleanEquals: ...
    #
    # def __eq__(self, other: Any) -> Type["ChoiceRule"]: ...
    #
    # @overload
    # def __ne__(self, other: Any) -> Not: ...
    #
    # @overload
    # def __gt__(self, other: Union[int, float, Decimal]) -> NumericGreaterThan: ...
    #
    # @overload
    # def __gt__(self, other: str) -> StringGreaterThan: ...
    #
    # @overload
    # def __gt__(self, other: datetime) -> TimestampGreaterThan: ...
    #
    # @overload
    # def __ge__(self, other: Union[int, float, Decimal]) -> NumericGreaterThanEquals: ...
    #
    # @overload
    # def __ge__(self, other: str) -> StringGreaterThanEquals: ...
    #
    # @overload
    # def __ge__(self, other: datetime) -> TimestampGreaterThanEquals: ...

VARIABLE_INPUT = Union[VariablePath, str, jsonpath_rw.JSONPath]
VARIABLE = VariablePath
NEXT = Optional[str]

class ChoiceRule:
    member_of: Optional[Choice]
    Value: NotImplemented
    Next: NotImplemented
    def then(self, state: StateMirror) -> StateMirror: ...
    def to_dict(self) -> Dict[str, Any]: ...

class StringEquals(ChoiceRule):
    def __init__(self, *, Value: str, Variable: VARIABLE_INPUT, Next: NEXT = None): ...
    Value: str
    Variable: VARIABLE
    Next: NEXT

class StringLessThan(ChoiceRule):
    def __init__(self, *, Value: str, Variable: VARIABLE_INPUT, Next: NEXT = None): ...
    Value: str
    Variable: VARIABLE
    Next: NEXT

class StringGreaterThan(ChoiceRule):
    def __init__(self, *, Value: str, Variable: VARIABLE_INPUT, Next: NEXT = None): ...
    Value: str
    Variable: VARIABLE
    Next: NEXT

class StringLessThanEquals(ChoiceRule):
    def __init__(self, *, Value: str, Variable: VARIABLE_INPUT, Next: NEXT = None): ...
    Value: str
    Variable: VARIABLE
    Next: NEXT

class StringGreaterThanEquals(ChoiceRule):
    def __init__(self, *, Value: str, Variable: VARIABLE_INPUT, Next: NEXT = None): ...
    Value: str
    Variable: VARIABLE
    Next: NEXT

class NumericEquals(ChoiceRule):
    def __init__(self, *, Value: Union[Decimal, float, int], Variable: VARIABLE_INPUT, Next: NEXT = None): ...
    Value: Decimal
    Variable: VARIABLE
    Next: NEXT

class NumericLessThan(ChoiceRule):
    def __init__(self, *, Value: Union[Decimal, float, int], Variable: VARIABLE_INPUT, Next: NEXT = None): ...
    Value: Decimal
    Variable: VARIABLE
    Next: NEXT

class NumericGreaterThan(ChoiceRule):
    def __init__(self, *, Value: Union[Decimal, float, int], Variable: VARIABLE_INPUT, Next: NEXT = None): ...
    Value: Decimal
    Variable: VARIABLE
    Next: NEXT

class NumericLessThanEquals(ChoiceRule):
    def __init__(self, *, Value: Union[Decimal, float, int], Variable: VARIABLE_INPUT, Next: NEXT = None): ...
    Value: Decimal
    Variable: VARIABLE
    Next: NEXT

class NumericGreaterThanEquals(ChoiceRule):
    def __init__(self, *, Value: Union[Decimal, float, int], Variable: VARIABLE_INPUT, Next: NEXT = None): ...
    Value: Decimal
    Variable: VARIABLE
    Next: NEXT

class BooleanEquals(ChoiceRule):
    def __init__(self, *, Value: bool, Variable: VARIABLE_INPUT, Next: NEXT = None): ...
    Value: bool
    Variable: VARIABLE
    Next: NEXT

class TimestampEquals(ChoiceRule):
    def __init__(self, *, Value: datetime, Variable: VARIABLE_INPUT, Next: NEXT = None): ...
    Value: datetime
    Variable: VARIABLE
    Next: NEXT

class TimestampLessThan(ChoiceRule):
    def __init__(self, *, Value: datetime, Variable: VARIABLE_INPUT, Next: NEXT = None): ...
    Value: datetime
    Variable: VARIABLE
    Next: NEXT

class TimestampGreaterThan(ChoiceRule):
    def __init__(self, *, Value: datetime, Variable: VARIABLE_INPUT, Next: NEXT = None): ...
    Value: datetime
    Variable: VARIABLE
    Next: NEXT

class TimestampLessThanEquals(ChoiceRule):
    def __init__(self, *, Value: datetime, Variable: VARIABLE_INPUT, Next: NEXT = None): ...
    Value: datetime
    Variable: VARIABLE
    Next: NEXT

class TimestampGreaterThanEquals(ChoiceRule):
    def __init__(self, *, Value: datetime, Variable: VARIABLE_INPUT, Next: NEXT = None): ...
    Value: datetime
    Variable: VARIABLE
    Next: NEXT

class And(ChoiceRule):
    def __init__(self, *, Rules: Iterable[ChoiceRule], Next: NEXT): ...
    Rules: Iterable[ChoiceRule]
    Next: NEXT

class Or(ChoiceRule):
    def __init__(self, *, Rules: Iterable[ChoiceRule], Next: NEXT): ...
    Rules: Iterable[ChoiceRule]
    Next: NEXT

class Not(ChoiceRule):
    def __init__(self, *, Rule: ChoiceRule, Next: NEXT): ...
    def to_dict(self, suppress_next: Optional[bool] = False) -> Dict[str, Any]: ...
    Rule: ChoiceRule
    Next: NEXT

def all_(*rules: ChoiceRule) -> And: ...
def any_(*rules: ChoiceRule) -> Or: ...
