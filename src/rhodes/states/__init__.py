""""""
import json
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Union

import attr
import jsonpath_rw
from attr.validators import deep_iterable, deep_mapping, instance_of, optional
from troposphere import Sub

from rhodes._converters import convert_to_json_path
from rhodes._runtime_types import TASK_RESOURCE_TYPES
from rhodes._serialization import serialize_name_and_value
from rhodes._util import RHODES_ATTRIB, RequiredValue, require_field
from rhodes._validators import is_valid_timestamp
from rhodes.choice_rules import ChoiceRule
from rhodes.exceptions import InvalidDefinitionError
from rhodes.structures import JsonPath

from ._parameters import _catch_retry, _input_output, _next_and_end, _parameters, _result_path, state, task_type

__all__ = ("State", "StateMachine", "Pass", "Parallel", "Map", "Choice", "Task", "Wait", "Fail", "Succeed")


@attr.s(eq=False)
class State:
    """Base class for states."""

    title: str = attr.ib(validator=instance_of(str))

    Comment: Optional[str] = RHODES_ATTRIB(validator=optional(instance_of(str)))

    member_of = None
    _required_fields: Iterable[RequiredValue] = []
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
        """Serialize state as a dictionary."""
        for required in self._required_fields:
            require_field(instance=self, required_value=required)

        self_dict = {"Type": self.Type}
        for field in attr.fields(type(self)):
            if field.name == "title":
                continue

            value = getattr(self, field.name)
            if value is None:
                continue

            new_name, new_value = serialize_name_and_value(name=field.name, value=value)

            self_dict[new_name] = new_value

        return self_dict

    def promote(self, path: Union[str, Enum, jsonpath_rw.JSONPath, JsonPath]) -> "Pass":
        """Add a :class:`Pass` state after this state that promotes a path in the input to this state's ``ResultPath``.

        Path *must* start with a path relative this state's ``ResultPath``
        as indicated by a ``@.`` prefix.

        :param path: Path to promote
        """
        # TODO: move this to the resultpath decorator?
        if not hasattr(self, "ResultPath"):
            raise AttributeError(f"{self.__class__.__name__} does not support 'promote'")

        path = convert_to_json_path(path)

        path_str = str(path)

        if not path_str.startswith("@."):
            raise ValueError("Promotion path must be relative (@.baz.wat)")

        input_path = JsonPath(f"{self.ResultPath}{path_str[1:]}")

        return self.then(Pass(f"{self.title}-PromoteResult", InputPath=input_path, ResultPath=self.ResultPath))


@attr.s
class StateMachine:
    """Step Functions State Machine.

    :param States: Map of states that make up this state machine
    :type States: dict(str, State)
    :param str StartAt: The state where this state machine starts
    :param str Comment: Human-readable description of the state
    :param str Version: The version of the Amazon States Language used in this state machine (must be ``1.0`` if provided)
    :param int TimeoutSeconds: Maximum time that this state machine is allowed to run
    """

    _required_fields = [
        RequiredValue("States", "State machine contains no states."),
        RequiredValue("StartAt", "State machine has no starting point."),
    ]
    __setup_complete = False

    States = RHODES_ATTRIB(
        default=attr.Factory(dict),
        validator=deep_mapping(key_validator=instance_of(str), value_validator=instance_of(State)),
    )
    # TODO: Name of State
    StartAt = RHODES_ATTRIB(validator=optional(instance_of(str)))
    Comment = RHODES_ATTRIB(validator=optional(instance_of(str)))
    # TODO: MUST be 1.0 if provided
    Version = RHODES_ATTRIB(validator=optional(instance_of(str)))
    # TODO: MUST be non-negative
    TimeoutSeconds = RHODES_ATTRIB(validator=optional(instance_of(int)))

    def __attrs_post_init__(self):
        self.__setup_complete = True

    def __setattr__(self, name, value):
        """Validate the value attribute value after setting."""
        super(StateMachine, self).__setattr__(name, value)
        if self.__setup_complete:
            # Don't validate until after attrs is done setting up.
            attr.validate(self)

    def to_dict(self) -> Dict:
        """Serialize this state machine as a dictionary."""
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
        """Serialize this state machine for use in a ``troposphere`` state machine definition."""
        data = self.to_dict()
        initial_value = json.dumps(data)
        return Sub(initial_value)

    def add_state(self, new_state: State) -> State:
        """Add a state to this state machine.

        :param State new_state: State to add
        """
        if new_state.title in self.States:
            if self.States[new_state.title] == new_state:
                return new_state

            raise InvalidDefinitionError(f"State {new_state.title!r} already in state machine.")

        new_state.member_of = self
        # TODO: use references rather than extracting names
        self.States[new_state.title] = new_state
        return new_state

    def start_with(self, first_state: State) -> State:
        """Add a state to this state machine and mark it as the starting state.

        :param State first_state: State to start with
        """
        self.add_state(new_state=first_state)

        # TODO: use references rather than extracting names
        self.StartAt = first_state.title

        return first_state


@attr.s(eq=False)
@_parameters
@_result_path
@_input_output
@_next_and_end
@state
class Pass(State):
    """"""

    Result = RHODES_ATTRIB()


@attr.s(eq=False)
@_parameters
@task_type
class Task(State):
    """"""

    _required_fields = [RequiredValue("Resource", "Task resource is not set.")]

    # TODO: Additional validation for strings?
    Resource = RHODES_ATTRIB(validator=optional(instance_of(TASK_RESOURCE_TYPES)))


@attr.s(eq=False)
@_input_output
@state
class Choice(State):
    """"""

    # TODO: Validate that Next and Default states are in parent
    # TODO: Choice does not allow
    Choices: List[ChoiceRule] = RHODES_ATTRIB(
        default=attr.Factory(list), validator=deep_iterable(member_validator=instance_of(ChoiceRule))
    )
    Default: Optional[str] = RHODES_ATTRIB(validator=optional(instance_of(str)))

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
@_input_output
@_next_and_end
@state
class Wait(State):
    """"""

    # TODO: Required only one of these on serialization

    Seconds: Optional[int] = RHODES_ATTRIB(validator=optional(instance_of(int)))
    # TODO: Timestamp must be ISO8601 timestamp
    # TODO: Just only accept datetime objects, like Timestamp choice rules
    Timestamp: Optional[str] = RHODES_ATTRIB()
    SecondsPath: Optional[JsonPath] = RHODES_ATTRIB(
        validator=optional(instance_of(JsonPath)), converter=convert_to_json_path
    )
    TimestampPath: Optional[JsonPath] = RHODES_ATTRIB(
        validator=optional(instance_of(JsonPath)), converter=convert_to_json_path
    )
    _exactly_one = ValueError(
        "Exactly one of 'Seconds', 'Timestamp', 'SecondsPath', and 'TimestampPath' must be supplied."
    )

    @Seconds.validator
    def _check_timestamp(self, attribute: attr.Attribute, value: Any):
        if value is None:
            return

        if not (self.Timestamp is self.SecondsPath is self.TimestampPath is None):
            raise self._exactly_one

    @Timestamp.validator
    def _check_timestamp(self, attribute: attr.Attribute, value: Any):
        if value is None:
            return

        if not is_valid_timestamp(value):
            raise ValueError(f"Invalid Timestamp value: {value}")

        if not (self.Seconds is self.SecondsPath is self.TimestampPath is None):
            raise self._exactly_one

    @SecondsPath.validator
    def _check_timestamp(self, attribute: attr.Attribute, value: Any):
        if value is None:
            return

        if not (self.Timestamp is self.Seconds is self.TimestampPath is None):
            raise self._exactly_one

    @TimestampPath.validator
    def _check_timestamp(self, attribute: attr.Attribute, value: Any):
        if value is None:
            return

        if not (self.Timestamp is self.Seconds is self.SecondsPath is None):
            raise self._exactly_one


@attr.s(eq=False)
@state
class Succeed(State):
    """"""


@attr.s(eq=False)
@state
class Fail(State):
    """"""

    Error: Optional[str] = RHODES_ATTRIB(validator=optional(instance_of(str)))
    Cause: Optional[str] = RHODES_ATTRIB(validator=optional(instance_of(str)))


@attr.s(eq=False)
@_parameters  # TODO: Spec and developer guide disagree on whether this is accepted...
@_catch_retry
@_result_path
@_input_output
@_next_and_end
@state
class Parallel(State):
    """"""

    # TODO: Each branch MUST be a self-contained state machine.
    Branches: List[StateMachine] = RHODES_ATTRIB(default=attr.Factory(list))

    def to_dict(self) -> Dict:
        self_dict = super(Parallel, self).to_dict()

        for pos, branch in enumerate(self_dict["Branches"]):
            self_dict["Branches"][pos] = branch.to_dict()

        return self_dict

    def add_branch(self, state_machine: Optional[StateMachine] = None) -> StateMachine:
        if state_machine is None:
            state_machine = StateMachine()

        self.Branches.append(state_machine)
        return state_machine


@attr.s(eq=False)
@_parameters
@_catch_retry
@_result_path
@_input_output
@_next_and_end
@state
class Map(State):
    """"""

    _required_fields = [
        RequiredValue("Iterator", "Map iterator must be set."),
        RequiredValue("ItemsPath", "Map items path must be set."),
    ]

    # TODO: Iterator MUST be a self-contained state machine.
    Iterator: StateMachine = RHODES_ATTRIB(validator=instance_of(StateMachine))
    # TODO: ItemsPath MUST be a valid JSON-path
    ItemsPath: JsonPath = RHODES_ATTRIB(validator=optional(instance_of(JsonPath)), converter=convert_to_json_path)
    # TODO: MaxConcurrency MUST be non-negative
    MaxConcurrency: Optional[int] = RHODES_ATTRIB(validator=optional(instance_of(int)))
