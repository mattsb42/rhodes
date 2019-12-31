from typing import Any, Dict, Iterable, List, Optional

import attr
from troposphere import Sub

from rhodes._types import (
    CATCH,
    COMMENT,
    END,
    HEARTBEAT_SECONDS,
    INPUT_PATH,
    NEXT,
    OUTPUT_PATH,
    PARAMETERS,
    PATH_INPUT,
    RESULT_PATH,
    RETRY,
    TASK_RESOURCE,
    TIMEOUT_SECONDS,
    TITLE,
    ChoiceRuleMirror,
    StateMachineMirror,
    StateMirror,
)
from rhodes._util import RequiredValue
from rhodes.choice_rules import ChoiceRule
from rhodes.structures import JsonPath

class State:
    def __init__(self, title: TITLE, *, Comment: COMMENT = None) -> None: ...
    Type: str
    member_of: Optional[StateMachine]
    title: TITLE
    Comment: COMMENT
    _required_fields: Iterable[RequiredValue]
    def to_dict(self) -> Dict: ...
    def promote(self, path: PATH_INPUT) -> Pass: ...

class StateMachine:
    def __init__(
        self,
        *,
        States: Dict[str, State] = attr.Factory(dict),
        StartAt: Optional[str] = None,
        Comment: COMMENT = None,
        Version: Optional[str] = None,
        TimeoutSeconds: TIMEOUT_SECONDS = None,
    ): ...
    States: Dict[str, State]
    StartAt: Optional[str]
    Comment: COMMENT
    Version: Optional[str]
    TimeoutSeconds: TIMEOUT_SECONDS
    _required_fields: Iterable[RequiredValue]
    def to_dict(self) -> Dict: ...
    def definition_string(self) -> Sub: ...
    def add_state(self, new_state: StateMirror) -> StateMirror: ...
    def start_with(self, first_state: StateMirror) -> StateMirror: ...

class Pass(State):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        Next: NEXT = None,
        End: END = None,
        InputPath: PATH_INPUT = JsonPath("$"),
        OutputPath: PATH_INPUT = JsonPath("$"),
        ResultPath: PATH_INPUT = JsonPath("$"),
        Parameters: PARAMETERS = None,
        Result: Optional[Any] = None,
    ) -> None: ...
    Next: NEXT
    End: END
    InputPath: INPUT_PATH
    OutputPath: OUTPUT_PATH
    ResultPath: RESULT_PATH
    Parameters: PARAMETERS
    Result: Optional[Any]
    def then(self, next_state: StateMirror) -> StateMirror: ...
    def end(self) -> Pass: ...

class Task(State):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        Next: NEXT = None,
        End: END = None,
        InputPath: PATH_INPUT = JsonPath("$"),
        OutputPath: PATH_INPUT = JsonPath("$"),
        ResultPath: PATH_INPUT = JsonPath("$"),
        Catch: CATCH = None,
        Retry: RETRY = None,
        TimeoutSeconds: TIMEOUT_SECONDS = None,
        HeartbeatSeconds: HEARTBEAT_SECONDS = None,
        Parameters: PARAMETERS = None,
        Resource: Optional[TASK_RESOURCE] = None,
    ): ...
    Next: NEXT
    End: END
    InputPath: INPUT_PATH
    OutputPath: OUTPUT_PATH
    ResultPath: RESULT_PATH
    Catch: CATCH
    Retry: RETRY
    TimeoutSeconds: TIMEOUT_SECONDS
    HeartbeatSeconds: HEARTBEAT_SECONDS
    Parameters: PARAMETERS
    Resource: Optional[TASK_RESOURCE]
    def then(self, next_state: StateMirror) -> StateMirror: ...
    def end(self) -> Task: ...

class Choice(State):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        InputPath: PATH_INPUT = JsonPath("$"),
        OutputPath: PATH_INPUT = JsonPath("$"),
        Choices: List[ChoiceRule] = attr.Factory(list),
        Default: Optional[str] = None,
    ): ...
    InputPath: INPUT_PATH
    OutputPath: OUTPUT_PATH
    Choices: List[ChoiceRule]
    Default: Optional[str]
    def add_choice(self, rule: ChoiceRuleMirror) -> ChoiceRuleMirror: ...
    def if_(self, rule: ChoiceRuleMirror) -> ChoiceRuleMirror: ...
    def else_(self, rule: StateMirror) -> StateMirror: ...

class Wait(State):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        Next: NEXT = None,
        End: END = None,
        InputPath: PATH_INPUT = JsonPath("$"),
        OutputPath: PATH_INPUT = JsonPath("$"),
        Seconds: Optional[int] = None,
        Timestamp: Optional[str] = None,
        SecondsPath: PATH_INPUT = JsonPath("$"),
        TimestampPath: PATH_INPUT = JsonPath("$"),
    ): ...
    Next: NEXT
    End: END
    InputPath: INPUT_PATH
    OutputPath: OUTPUT_PATH
    Seconds: Optional[int]
    Timestamp: Optional[str]
    SecondsPath: Optional[JsonPath]
    TimestampPath: Optional[JsonPath]
    def then(self, next_state: StateMirror) -> StateMirror: ...
    def end(self) -> Wait: ...

class Succeed(State): ...

class Fail(State):
    def __init__(
        self, title: TITLE, *, Comment: COMMENT = None, Error: Optional[str] = None, Cause: Optional[str] = None
    ): ...
    Error: Optional[str]
    Cause: Optional[str]

class Parallel(State):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        Next: NEXT = None,
        End: END = None,
        InputPath: PATH_INPUT = JsonPath("$"),
        OutputPath: PATH_INPUT = JsonPath("$"),
        ResultPath: PATH_INPUT = JsonPath("$"),
        Catch: CATCH = None,
        Retry: RETRY = None,
        Parameters: PARAMETERS = None,
        Branches: List[StateMachine] = attr.Factory(list),
    ): ...
    Next: NEXT
    End: END
    InputPath: INPUT_PATH
    OutputPath: OUTPUT_PATH
    ResultPath: RESULT_PATH
    Catch: CATCH
    Retry: RETRY
    Parameters: PARAMETERS
    Branches: List[StateMachine]
    def then(self, next_state: StateMirror) -> StateMirror: ...
    def end(self) -> Parallel: ...
    def add_branch(self, state_machine: Optional[StateMachineMirror]) -> StateMachineMirror: ...

class Map(State):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        Next: NEXT = None,
        End: END = None,
        InputPath: PATH_INPUT = JsonPath("$"),
        OutputPath: PATH_INPUT = JsonPath("$"),
        ResultPath: PATH_INPUT = JsonPath("$"),
        Catch: CATCH = None,
        Retry: RETRY = None,
        Parameters: PARAMETERS = None,
        Iterator: Optional[StateMachine] = None,
        ItemsPath: PATH_INPUT = JsonPath("$"),
        MaxConcurrency: Optional[int] = None,
    ): ...
    Next: NEXT
    End: END
    InputPath: INPUT_PATH
    OutputPath: OUTPUT_PATH
    ResultPath: RESULT_PATH
    Catch: CATCH
    Retry: RETRY
    Parameters: PARAMETERS
    Iterator: Optional[StateMachine]
    ItemsPath: Optional[JsonPath]
    MaxConcurrency: Optional[int]
    def then(self, next_state: StateMirror) -> StateMirror: ...
    def end(self) -> Map: ...
