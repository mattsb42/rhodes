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

class AmazonEcs(State):
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
        Cluster: Optional[Any] = None,
        Group: Optional[Any] = None,
        LaunchType: Optional[Any] = None,
        NetworkConfiguration: Optional[Any] = None,
        Overrides: Optional[Any] = None,
        PlacementConstraints: Optional[Any] = None,
        PlacementStrategy: Optional[Any] = None,
        PlatformVersion: Optional[Any] = None,
        TaskDefinition: Optional[Any] = None,
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
    Pattern: IntegrationPattern
    Cluster: Optional[Any]
    Group: Optional[Any]
    LaunchType: Optional[Any]
    NetworkConfiguration: Optional[Any]
    Overrides: Optional[Any]
    PlacementConstraints: Optional[Any]
    PlacementStrategy: Optional[Any]
    PlatformVersion: Optional[Any]
    TaskDefinition: Optional[Any]
