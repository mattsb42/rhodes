"""
Standard Step Functions and state machine states.

`See Step Functions docs for more details.
<https://docs.aws.amazon.com/step-functions/latest/dg/concepts-states.html>`_

"""
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

    `See Step Functions docs for more details.
    <https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-state-machine-structure.html>`_

    :param States: Map of states that make up this state machine
    :type States: dict(str, State)
    :param str StartAt: The state where this state machine starts
    :param str Comment: Human-readable description of the state
    :param str Version: The version of the Amazon States Language used in this state machine
      (must be ``1.0`` if provided)
    :param int TimeoutSeconds: Maximum time that this state machine is allowed to run
    """

    _required_fields = [
        RequiredValue("States", "State machine contains no states."),
        RequiredValue("StartAt", "State machine has no starting point."),
    ]
    __setup_complete = False

    States: Dict[str, State] = RHODES_ATTRIB(
        default=attr.Factory(dict),
        validator=deep_mapping(key_validator=instance_of(str), value_validator=instance_of(State)),
    )
    # TODO: Name of State
    StartAt: Optional[str] = RHODES_ATTRIB(validator=optional(instance_of(str)))
    Comment: Optional[str] = RHODES_ATTRIB(validator=optional(instance_of(str)))
    # TODO: MUST be 1.0 if provided
    Version: Optional[str] = RHODES_ATTRIB(validator=optional(instance_of(str)))
    # TODO: MUST be non-negative
    TimeoutSeconds: Optional[int] = RHODES_ATTRIB(validator=optional(instance_of(int)))

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
    """A Pass state passes its input to its output without performing work.
    Pass states are useful when constructing and debugging state machines.

    `See Step Functions docs for more details.
    <https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-pass-state.html>`_

    """

    Result = RHODES_ATTRIB()


@attr.s(eq=False)
@_parameters
@task_type
class Task(State):
    """A Task state represents a single unit of work performed by a state machine.

    `See Step Functions docs for more details.
    <https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-task-state.html>`_

    """

    _required_fields = [RequiredValue("Resource", "Task resource is not set.")]

    # TODO: Additional validation for strings?
    Resource = RHODES_ATTRIB(validator=optional(instance_of(TASK_RESOURCE_TYPES)))


@attr.s(eq=False)
@_input_output
@state
class Choice(State):
    """A Choice state adds branching logic to a state machine.

    `See Step Functions docs for more details.
    <https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-choice-state.html>`_

    .. code-block:: python

        workflow = StateMachine()

        next_state = Pass("Ok number")

        decision = workflow.start_with(Choice("Make a decision"))
        decision.if_(VariablePath("$.foo.bar") == 12).then(next_state)
        decision.if_(VariablePath("$.foo.bar") < 0).then(Fail("Negative value!"))
        decision.if_(all_(
            VariablePath("$.foo.bar") != 12,
            VariablePath("$.baz.wow") == "not 12!",
        )).then(next_state)
        decision.else_(Succeed("Something else!"))

        next_state.end()

    .. code-block:: json

        {
            "States": {
                "Make a decision": {
                    "Type": "Choice",
                    "Choices": [
                        {
                            "Variable": "$.foo.bar",
                            "NumericEquals": 12,
                            "Next": "Ok number"
                        },
                        {
                            "Variable": "$.foo.bar",
                            "NumericLessThan": 0,
                            "Next": "Negative value!"
                        },
                        {
                            "And": [
                                {
                                    "Not": {
                                        "Variable": "$.foo.bar",
                                        "NumericEquals": 12
                                    }
                                },
                                {
                                    "Variable": "$.baz.wow",
                                    "StringEquals": "not 12!"
                                }
                            ],
                            "Next": "Ok number"
                        }
                    ],
                    "Default": "Something else!"
                },
                "Ok number": {
                    "Type": "Pass",
                    "End": true
                },
                "Negative value!": {
                    "Type": "Fail"
                },
                "Something else!": {
                    "Type": "Succeed"
                }
            }
        }

    """

    Choices: List[ChoiceRule] = RHODES_ATTRIB(
        default=attr.Factory(list), validator=deep_iterable(member_validator=instance_of(ChoiceRule))
    )
    Default: Optional[str] = RHODES_ATTRIB(validator=optional(instance_of(str)))

    def add_choice(self, rule: ChoiceRule) -> ChoiceRule:
        """Add a choice rule to this state.
        This is the lower-level interface that :method:`if_` uses.

        :param rule: Rule to add
        :return: ``rule``
        """
        if rule.member_of is not None:
            if rule.member_of is self:
                return rule

            raise InvalidDefinitionError("Rule already added to another Choice state")

        self.Choices.append(rule)
        rule.member_of = self
        return rule

    def if_(self, rule: ChoiceRule) -> ChoiceRule:
        """Add a choice rule to this state as one possible logic branch.
        This should be followed up with a ``.then(STATE)`` call.

        .. code-block:: python

            decision.if_(VariablePath("$.foo.bar") == 12).then(next_state)

        This results in the rule definition:

        .. code-block:: json

            {
                "Variable": "$.foo.bar",
                "NumericEquals": 12,
                "Next": "NEXT_STATE_NAME"
            }

        :param rule: The rule to add
        :returns: ``rule``
        """
        return self.add_choice(rule)

    def else_(self, state: State) -> State:
        """Add a default state.
        This is the state to transition to if none of the choice rules are satisfied.

        :param state: The default state to add
        :return: ``state``
        """
        if self.Default is not None:
            raise InvalidDefinitionError(f'Choice state "{self.title}" already has a Default transition.')

        self.member_of.add_state(state)

        # TODO: use references rather than extracting names
        self.Default = state.title

        return state

    def to_dict(self) -> Dict:
        """Serialize state as a dictionary."""
        if not self.Choices:
            raise InvalidDefinitionError(f"Choice state '{self.title}' has no defined choices.")

        if self.member_of is not None and self.Default not in self.member_of.States:
            raise InvalidDefinitionError(
                f"Default state '{self.Default}' for Choice state '{self.title}' is not present in state machine."
            )

        self_dict = super(Choice, self).to_dict()

        for pos, branch in enumerate(self_dict["Choices"]):
            self_dict["Choices"][pos] = branch.to_dict()
            if self.member_of is not None and branch.Next not in self.member_of.States:
                raise InvalidDefinitionError(
                    f"Choice rule next state '{branch.Next}' "
                    f"for Choice state '{self.title}' is not present in state machine."
                )

        return self_dict


@attr.s(eq=False)
@_input_output
@_next_and_end
@state
class Wait(State):
    """A Wait state delays the state machine from continuing for a specified time.
    You can choose either a relative time,
    specified in seconds from when the state begins,
    or an absolute end time, specified as a timestamp.

    `See Step Functions docs for more details.
    <https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-wait-state.html>`_

    """

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
        # pylint: disable=no-self-use,unused-argument
        if value is None:
            return

        if not self.Timestamp is self.SecondsPath is self.TimestampPath is None:
            raise self._exactly_one

    @Timestamp.validator
    def _check_timestamp(self, attribute: attr.Attribute, value: Any):
        # pylint: disable=no-self-use,unused-argument
        if value is None:
            return

        if not is_valid_timestamp(value):
            raise ValueError(f"Invalid Timestamp value: {value}")

        if not self.Seconds is self.SecondsPath is self.TimestampPath is None:
            raise self._exactly_one

    @SecondsPath.validator
    def _check_timestamp(self, attribute: attr.Attribute, value: Any):
        # pylint: disable=no-self-use,unused-argument
        if value is None:
            return

        if not self.Timestamp is self.Seconds is self.TimestampPath is None:
            raise self._exactly_one

    @TimestampPath.validator
    def _check_timestamp(self, attribute: attr.Attribute, value: Any):
        # pylint: disable=no-self-use,unused-argument
        if value is None:
            return

        if not self.Timestamp is self.Seconds is self.SecondsPath is None:
            raise self._exactly_one


@attr.s(eq=False)
@state
class Succeed(State):
    """A Succeed state stops an execution successfully.
    The Succeed state is a useful target for Choice state branches that don't do anything but stop the execution.

    `See Step Functions docs for more details.
    <https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-succeed-state.html>`_

    """


@attr.s(eq=False)
@state
class Fail(State):
    """A Fail state stops the execution of the state machine and marks it as a failure.

    `See Step Functions docs for more details.
    <https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-fail-state.html>`_

    """

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
    """The Parallel state can be used to create parallel branches of execution in your state machine.

    `See Step Functions docs for more details.
    <https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-parallel-state.html>`_

    """

    # TODO: Each branch MUST be a self-contained state machine.
    Branches: List[StateMachine] = RHODES_ATTRIB(default=attr.Factory(list))

    def to_dict(self) -> Dict:
        """Serialize state as a dictionary."""
        self_dict = super(Parallel, self).to_dict()

        for pos, branch in enumerate(self_dict["Branches"]):
            self_dict["Branches"][pos] = branch.to_dict()

        return self_dict

    def add_branch(self, state_machine: Optional[StateMachine] = None) -> StateMachine:
        """Add a parallel branch to this state.
        If ``state_machine`` is not provided, we generate an empty state machine and add that.

        :param state_machine: State machine to add (optional)
        :return: ``state_machine`` if provided or a new empty state machine if not
        """
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
    """The Map state can be used to run a set of steps for each element of an input array.
    While the Parallel state executes multiple branches of steps using the same input,
    a Map state will execute the same steps for multiple entries of an array in the state input.

    `See Step Functions docs for more details.
    <https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-map-state.html>`_

    """

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
