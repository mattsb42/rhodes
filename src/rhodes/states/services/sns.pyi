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
    TIMEOUT_SECONDS,
    TITLE,
    StateMirror,
)
from rhodes.identifiers import IntegrationPattern
from rhodes.states import State
from rhodes.structures import JsonPath

class AmazonSns(State):
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
        Message: Optional[Any] = None,
        MessageAttributes: Optional[Any] = None,
        MessageStructure: Optional[Any] = None,
        Subject: Optional[Any] = None,
        PhoneNumber: Optional[Any] = None,
        TargetArn: Optional[Any] = None,
        TopicArn: Optional[Any] = None,
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
    Message: Optional[Any]
    MessageAttributes: Optional[Any]
    MessageStructure: Optional[Any]
    Subject: Optional[Any]
    PhoneNumber: Optional[Any]
    TargetArn: Optional[Any]
    TopicArn: Optional[Any]
    Pattern: IntegrationPattern
