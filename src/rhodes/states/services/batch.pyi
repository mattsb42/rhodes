from typing import Any, Optional

from rhodes._types import (
    CATCH,
    COMMENT,
    END,
    HEARTBEAT_SECONDS,
    INPUT_PATH,
    NEXT,
    OUTPUT_PATH,
    PATH_INPUT,
    RESULT_PATH,
    RETRY,
    SERVICE_INTEGRATION_COMPLEX_VALUE,
    SERVICE_INTEGRATION_SIMPLE_VALUE,
    TIMEOUT_SECONDS,
    TITLE,
    StateMirror,
)
from rhodes.identifiers import IntegrationPattern
from rhodes.states import State
from rhodes.structures import JsonPath, Parameters

class AwsBatch(State):
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
        JobDefinition: Optional[Any] = None,
        JobName: Optional[Any] = None,
        JobQueue: Optional[Any] = None,
        Parameters: Parameters = None,
        ArrayProperties: Optional[Any] = None,
        ContainerOverrides: Optional[Any] = None,
        DependsOn: Optional[Any] = None,
        RetryStrategy: Optional[Any] = None,
        Timeout: Optional[Any] = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
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
    def then(self, next_state: StateMirror) -> StateMirror: ...
    def end(self) -> State: ...
    JobDefinition: Optional[Any]
    JobName: Optional[Any]
    JobQueue: Optional[Any]
    Parameters: Parameters
    ArrayProperties: Optional[Any]
    ContainerOverrides: Optional[Any]
    DependsOn: Optional[Any]
    RetryStrategy: Optional[Any]
    Timeout: Optional[Any]
    Pattern: IntegrationPattern
