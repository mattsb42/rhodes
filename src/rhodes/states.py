""""""
from typing import Dict, Optional

import attr
from attr.validators import deep_iterable, deep_mapping, instance_of, optional

from ._util import RequiredValue, require_field
from ._validators import is_valid_arn, is_valid_timestamp
from .choice_rules import ChoiceRule
from .exceptions import InvalidDefinitionError


@attr.s(eq=False)
class State:
    """"""

    name = attr.ib(validator=instance_of(str))
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
            return False

        if self.to_dict() != other.to_dict():
            return False

        if self.member_of != other.member_of:
            return False

        return True

    def __ne__(self, other: "State") -> bool:
        return not self.__eq__(other)

    def to_dict(self) -> Dict:
        self_dict = {"Type": self.Type}
        for field in attr.fields(type(self)):
            if field.name == "name":
                continue

            value = getattr(self, field.name)
            if value is None:
                continue

            if hasattr(value, "to_dict") and callable(value.to_dict):
                self_dict[field.name] = value.to_dict()
                continue

            self_dict[field.name] = value

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

    def add_state(self, new_state: State) -> State:
        if new_state.name in self.States:
            if self.States[new_state.name] == new_state:
                return new_state

            raise InvalidDefinitionError(f"State {new_state.name!r} already in state machine.")

        new_state.member_of = self
        # TODO: use references rather than extracting names
        self.States[new_state.name] = new_state
        return new_state

    def start_with(self, first_state: State) -> State:
        self.add_state(new_state=first_state)

        # TODO: use references rather than extracting names
        self.StartAt = first_state.name

        return first_state


def _comment(cls):
    cls.Comment = attr.ib(default=None, validator=optional(instance_of(str)))

    return cls


def _input_output(cls):
    cls.InputPath = attr.ib(default=None, validator=optional(instance_of(str)))
    cls.OutputPath = attr.ib(default=None, validator=optional(instance_of(str)))

    return cls


def _parameters(cls):
    cls.Parameters = attr.ib(default=None, validator=optional(instance_of(str)))

    return cls


def _result_path(cls):
    cls.ResultPath = attr.ib(default=None, validator=optional(instance_of(str)))

    return cls


def _next_or_end(cls):
    # TODO: These need to be required and exclusive OR
    cls.Next = attr.ib(default=None, validator=optional(instance_of(str)))
    # TODO: End=False is invalid
    cls.End = attr.ib(default=None, validator=optional(instance_of(bool)))

    def _set_next(instance: State, next_state: State) -> State:
        if instance.End:
            raise InvalidDefinitionError(
                "Cannot set state transition." f"State {instance.name!r} already has an end condition."
            )

        instance.member_of.add_state(next_state)
        # TODO: set reference rather than extracting name
        instance.Next = next_state.name
        return next_state

    def _set_end(instance: State) -> State:
        if instance.Next:
            raise InvalidDefinitionError(
                "Cannot set end condition." f"State {instance.name!r} already has a state transition."
            )

        instance.End = True

        return instance

    cls.then = _set_next
    cls.end = _set_end

    return cls


def _catch_retry(cls):
    cls.Retry = attr.ib(default=None)
    cls.Catch = attr.ib(default=None)

    return cls


@attr.s(eq=False)
@_comment
@_input_output
@_parameters
@_result_path
@_next_or_end
class Pass(State):
    Result = attr.ib(default=None)


@attr.s(eq=False)
@_comment
@_input_output
@_parameters
@_result_path
@_next_or_end
@_catch_retry
class Task(State):
    _required_fields = [RequiredValue("Resource", "Task resource is not set.")]

    # TODO: Resource MUST be a URI
    # TODO: Support CloudFormation references
    Resource = attr.ib(default=None, validator=optional(instance_of(str)))
    # TODO: Timeout MUST be positive
    TimeoutSeconds = attr.ib(default=None, validator=optional(instance_of(int)))
    # TODO: HeartbeatSeconds MUST be positive
    HeartbeatSeconds = attr.ib(default=None, validator=optional(instance_of(int)))

    @Resource.validator
    def _check_resource(self, attribute, value):
        if not is_valid_arn(value):
            raise ValueError("Invalid Arn: {}".format(value))


@attr.s(eq=False)
@_comment
@_input_output
class Choice(State):
    # TODO: Validate that Next and Default states are in parent
    Choices = attr.ib(default=attr.Factory(list), validator=deep_iterable(member_validator=instance_of(ChoiceRule)))
    Default = attr.ib(default=None)

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
            raise InvalidDefinitionError(f'Choice state "{self.name}" already has a Default transition.')

        self.member_of.add_state(state)

        # TODO: use references rather than extracting names
        self.Default = state.name

        return state

    def to_dict(self) -> Dict:
        if not self.Choices:
            raise InvalidDefinitionError(f'Choice state "{self.name}" has no defined choices.')

        self_dict = super(Choice, self).to_dict()

        for pos, branch in enumerate(self_dict["Choices"]):
            self_dict["Choices"][pos] = branch.to_dict()

        return self_dict


@attr.s(eq=False)
@_comment
@_input_output
@_next_or_end
class Wait(State):
    # TODO: Exactly one of these
    Seconds = attr.ib(default=None, validator=optional(instance_of(int)))
    # TODO: Timestamp must be ISO8601 timestamp
    Timestamp = attr.ib(default=None)
    # TODO: Paths MUST be valid JSON-paths
    SecondsPath = attr.ib(default=None, validator=optional(instance_of(str)))
    TimestampPath = attr.ib(default=None, validator=optional(instance_of(str)))

    @Timestamp.validator
    def _check_timestamp(self, attribute, value):
        if not is_valid_timestamp(value):
            raise ValueError("Invalid Timestamp value: {}".format(value))


@attr.s(eq=False)
@_comment
@_input_output
class Succeed(State):
    """"""


@attr.s(eq=False)
@_comment
class Fail(State):
    """"""

    Error = attr.ib(default=None, validator=optional(instance_of(str)))
    Cause = attr.ib(default=None, validator=optional(instance_of(str)))


@attr.s(eq=False)
@_comment
@_input_output
@_parameters
@_result_path
@_next_or_end
@_catch_retry
class Parallel(State):
    # TODO: Each branch MUST be a self-contained state machine.
    Branches = attr.ib(default=attr.Factory(list))

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
@_comment
@_input_output
@_parameters
@_result_path
@_next_or_end
@_catch_retry
class Map(State):
    # TODO: Iterator MUST be a self-contained state machine.
    Iterator = attr.ib()
    # TODO: ItemsPath MUST be a valid JSON-path
    ItemsPath = attr.ib()
    # TODO: MaxConcurrency MUST be non-negative
    MaxConcurrency = attr.ib(default=None, validator=optional(instance_of(int)))
