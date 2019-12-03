""""""
import json
from typing import Any, Dict, Optional, Iterable

import attr
from attr.validators import deep_iterable, deep_mapping, instance_of, optional
from troposphere import GetAtt, Ref, Sub, awslambda, stepfunctions

from rhodes._converters import convert_to_json_path
from rhodes._util import RequiredValue, require_field
from rhodes._validators import is_valid_arn, is_valid_timestamp
from rhodes.choice_rules import ChoiceRule
from rhodes.exceptions import InvalidDefinitionError
from rhodes.structures import ContextPath, JsonPath

__all__ = (
    "State",
    "StateMachine",
    "Pass",
    "Parameters",
    "Parallel",
    "Map",
    "Choice",
    "Task",
    "Wait",
    "Fail",
    "Succeed",
)


def _getatt_arn(value: str) -> str:
    return f"${{{value}.Arn}}"


def _ref(value: str) -> str:
    return f"${{{value}}}"


def _serialize_troposphere_value(value):
    # Inject appropriate Ref/GetAtt for Troposphere
    if isinstance(value, awslambda.Function):
        return _getatt_arn(value.title)

    if isinstance(value, stepfunctions.Activity):
        return _ref(value.title)

    if isinstance(value, Ref):
        return _ref(value.data["Ref"])

    if isinstance(value, GetAtt):
        return _getatt_arn(value.data["Fn::GetAtt"][0])

    return value


def _serialize_name_and_value(*, name: str, value: Any) -> [str, Any]:
    value = _serialize_troposphere_value(value)

    if isinstance(value, (JsonPath, ContextPath)):
        return name, str(value)

    if hasattr(value, "to_dict") and callable(value.to_dict):
        return name, value.to_dict()

    return name, value


@attr.s(eq=False)
class State:
    """"""

    title: str = attr.ib(validator=instance_of(str))
    # TODO: These need to be required and exclusive OR
    Next: str = attr.ib(default=None, validator=optional(instance_of(str)))
    # TODO: End=False is invalid
    End: bool = attr.ib(default=None, validator=optional(instance_of(bool)))
    Comment: Optional[str] = attr.ib(default=None, validator=optional(instance_of(str)))
    InputPath: Optional[JsonPath] = attr.ib(default=None, validator=optional(instance_of(JsonPath)), converter=convert_to_json_path)
    OutputPath: Optional[JsonPath] = attr.ib(default=None, validator=optional(instance_of(JsonPath)), converter=convert_to_json_path)

    def then(self: "State", next_state: "State") -> "State":
        if self.End:
            raise InvalidDefinitionError(
                "Cannot set state transition." f"State {self.title!r} already has an end condition."
            )

        self.member_of.add_state(next_state)
        # TODO: set reference rather than extracting name
        self.Next = next_state.title
        return next_state

    def end(self: "State") -> "State":
        if self.Next:
            raise InvalidDefinitionError(
                "Cannot set end condition." f"State {self.title!r} already has a state transition."
            )

        self.End = True

        return self

    member_of = None
    _required_fields = []
    __setup_complete = False

    def __attrs_post_init__(self):
        self.Type = self.__class__.__name__
        self.__setup_complete = True

    def __setattr__(self, name, value):
        """Validate the value attribute value after setting."""
        super(State, self).__setattr__(name, value)
        if self.__setup_complete:
            # Don't validate until after attrs is done setting up.
            attr.validate(self)

    def __eq__(self, other: "State") -> bool:
        if not isinstance(other, self.__class__):
            # TODO: What about the other direction?
            #  ex: Child() == Parent() vs Parent() == Child()
            return False

        if self.to_dict() != other.to_dict():
            return False

        if self.member_of != other.member_of:
            return False

        return True

    def __ne__(self, other: "State") -> bool:
        return not self.__eq__(other)

    def to_dict(self) -> Dict:
        for required in self._required_fields:
            require_field(instance=self, required_value=required)

        self_dict = {"Type": self.Type}
        for field in attr.fields(type(self)):
            if field.name == "title":
                continue

            value = getattr(self, field.name)
            if value is None:
                continue

            new_name, new_value = _serialize_name_and_value(name=field.name, value=value)

            self_dict[new_name] = new_value

        return self_dict


@attr.s
class StateMachine:
    """"""

    _required_fields = [
        RequiredValue("States", "State machine contains no states."),
        RequiredValue("StartAt", "State machine has no starting point."),
    ]
    __setup_complete = False

    # TODO: Map of States
    States = attr.ib(
        default=attr.Factory(dict),
        validator=deep_mapping(key_validator=instance_of(str), value_validator=instance_of(State)),
    )
    # TODO: Name of State
    StartAt = attr.ib(default=None, validator=optional(instance_of(str)))
    Comment = attr.ib(default=None, validator=optional(instance_of(str)))
    # TODO: MUST be 1.0 if provided
    Version = attr.ib(default=None, validator=optional(instance_of(str)))
    # TODO: MUST be non-negative
    TimeoutSeconds = attr.ib(default=None, validator=optional(instance_of(int)))

    def __attrs_post_init__(self):
        self.__setup_complete = True

    def __setattr__(self, name, value):
        """Validate the value attribute value after setting."""
        super(StateMachine, self).__setattr__(name, value)
        if self.__setup_complete:
            # Don't validate until after attrs is done setting up.
            attr.validate(self)

    def to_dict(self) -> Dict:
        for required in self._required_fields:
            require_field(instance=self, required_value=required)

        if self.StartAt not in self.States:
            raise InvalidDefinitionError(f"Starting state {self.StartAt!r} not in states {self.States.keys()!r}.")

        self_dict = dict(StartAt=self.StartAt)

        for optional_attribute in ("Comment", "TimeoutSeconds", "Version"):
            if getattr(self, optional_attribute) is not None:
                self_dict[optional_attribute] = getattr(self, optional_attribute)

        self_dict["States"] = {key: value.to_dict() for key, value in self.States.items()}

        return self_dict

    def definition_string(self) -> Sub:
        data = self.to_dict()
        initial_value = json.dumps(data)
        return Sub(initial_value)

    def add_state(self, new_state: State) -> State:
        if new_state.title in self.States:
            if self.States[new_state.title] == new_state:
                return new_state

            raise InvalidDefinitionError(f"State {new_state.title!r} already in state machine.")

        new_state.member_of = self
        # TODO: use references rather than extracting names
        self.States[new_state.title] = new_state
        return new_state

    def start_with(self, first_state: State) -> State:
        self.add_state(new_state=first_state)

        # TODO: use references rather than extracting names
        self.StartAt = first_state.title

        return first_state


class Parameters:
    def __init__(self, **kwargs):
        self._map = kwargs

    def to_dict(self) -> Dict[str, Any]:
        def _inner():
            for name, value in self._map.items():
                new_name, new_value = _serialize_name_and_value(name=name, value=value)

                if isinstance(value, JsonPath) or isinstance(value, ContextPath):
                    # If you manually provide path strings, you must manually set the parameter suffix.
                    if not new_name.endswith(".$"):
                        new_name += ".$"

                yield new_name, new_value

        return dict(_inner())

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{name}={value!r}' for name, value in self._map.items())})"


def _parameters(cls):
    cls.Parameters = attr.ib(default=None, validator=optional(instance_of(Parameters)))

    return cls


def _result_path(cls):
    cls.ResultPath = attr.ib(default=None, validator=optional(instance_of(JsonPath)), converter=convert_to_json_path)

    return cls


def _catch_retry(cls):
    cls.Retry = attr.ib(default=None)
    cls.Catch = attr.ib(default=None)

    return cls


@attr.s(eq=False)
@_parameters
@_result_path
class Pass(State):
    Result = attr.ib(default=None)


def task_type(cls):
    cls = _catch_retry(cls)
    cls = _result_path(cls)

    # TODO: Timeout MUST be positive
    cls.TimeoutSeconds = attr.ib(default=None, validator=optional(instance_of(int)))
    # TODO: HeartbeatSeconds MUST be positive
    cls.HeartbeatSeconds = attr.ib(default=None, validator=optional(instance_of(int)))

    return cls


@attr.s(eq=False)
@_parameters
@task_type
class Task(State):
    _required_fields = [RequiredValue("Resource", "Task resource is not set.")]

    # TODO: Additional validation for strings?
    Resource = attr.ib(
        default=None, validator=optional(instance_of((str, awslambda.Function, stepfunctions.Activity, GetAtt, Ref)))
    )


@attr.s(eq=False)
class Choice(State):
    # TODO: Validate that Next and Default states are in parent
    Choices: Iterable[ChoiceRule] = attr.ib(default=attr.Factory(list), validator=deep_iterable(member_validator=instance_of(ChoiceRule)))
    Default: Optional[str] = attr.ib(default=None, validator=optional(instance_of(str)))

    def add_choice(self, rule: ChoiceRule) -> ChoiceRule:
        if rule.member_of is not None:
            if rule.member_of is self:
                return rule

            raise InvalidDefinitionError("Rule already added to another Choice state")

        self.Choices.append(rule)
        rule.member_of = self
        return rule

    def if_(self, rule: ChoiceRule) -> ChoiceRule:
        return self.add_choice(rule)

    def else_(self, state: State) -> State:
        if self.Default is not None:
            raise InvalidDefinitionError(f'Choice state "{self.title}" already has a Default transition.')

        self.member_of.add_state(state)

        # TODO: use references rather than extracting names
        self.Default = state.title

        return state

    def to_dict(self) -> Dict:
        if not self.Choices:
            raise InvalidDefinitionError(f'Choice state "{self.title}" has no defined choices.')

        self_dict = super(Choice, self).to_dict()

        for pos, branch in enumerate(self_dict["Choices"]):
            self_dict["Choices"][pos] = branch.to_dict()

        return self_dict


@attr.s(eq=False)
class Wait(State):
    # TODO: Exactly one of these
    Seconds: Optional[int] = attr.ib(default=None, validator=optional(instance_of(int)))
    # TODO: Timestamp must be ISO8601 timestamp
    # TODO: Just only accept datetime objects, like Timestamp choice rules
    Timestamp: Optional[str] = attr.ib(default=None)
    SecondsPath: Optional[JsonPath] = attr.ib(default=None, validator=optional(instance_of(JsonPath)), converter=convert_to_json_path)
    TimestampPath: Optional[JsonPath] = attr.ib(default=None, validator=optional(instance_of(JsonPath)), converter=convert_to_json_path)

    @Timestamp.validator
    def _check_timestamp(self, attribute, value):
        if not is_valid_timestamp(value):
            raise ValueError("Invalid Timestamp value: {}".format(value))


@attr.s(eq=False)
class Succeed(State):
    """"""
    # TODO: Succeed does not accept any of the parent parameters...


@attr.s(eq=False)
class Fail(State):
    """"""
    # TODO: The only parent parameter that Fail accepts is Comment

    Error: Optional[str] = attr.ib(default=None, validator=optional(instance_of(str)))
    Cause: Optional[str] = attr.ib(default=None, validator=optional(instance_of(str)))


@attr.s(eq=False)
@_parameters  # TODO: Spec and developer guide disagree on whether this is accepted...
@_result_path
@_catch_retry
class Parallel(State):
    # TODO: Each branch MUST be a self-contained state machine.
    Branches: Iterable[StateMachine] = attr.ib(default=attr.Factory(list))

    def to_dict(self) -> Dict:
        self_dict = super(Parallel, self).to_dict()

        for pos, branch in enumerate(self_dict["Branches"]):
            self_dict["Branches"][pos] = branch.to_dict()

        return self_dict

    def add_branch(self, state_machine: Optional[StateMachine] = None):
        if state_machine is None:
            state_machine = StateMachine()

        self.Branches.append(state_machine)
        return state_machine


@attr.s(eq=False)
@_parameters
@_result_path
@_catch_retry
class Map(State):
    _required_fields = [
        RequiredValue("Iterator", "Map iterator must be set."),
        RequiredValue("ItemsPath", "Map items path must be set.")
    ]

    # TODO: Iterator MUST be a self-contained state machine.
    Iterator: StateMachine = attr.ib(default=None, validator=instance_of(StateMachine))
    # TODO: ItemsPath MUST be a valid JSON-path
    ItemsPath: JsonPath = attr.ib(default=None, validator=optional(instance_of(JsonPath)), converter=convert_to_json_path)
    # TODO: MaxConcurrency MUST be non-negative
    MaxConcurrency: Optional[int] = attr.ib(default=None, validator=optional(instance_of(int)))
