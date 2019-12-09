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
    State,
    StateMirror,
)
from rhodes.structures import JsonPath

class ServiceIntegration(State):
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
    def end(self) -> ServiceIntegration: ...
