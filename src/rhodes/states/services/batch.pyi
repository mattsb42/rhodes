from typing import Any, Optional

from rhodes._types import CATCH, COMMENT, END, HEARTBEAT_SECONDS, NEXT, PATH_INPUT, RETRY, TIMEOUT_SECONDS, TITLE
from rhodes.identifiers import IntegrationPattern
from rhodes.states.services import ServiceIntegration
from rhodes.structures import Parameters

class AwsBatch(ServiceIntegration):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        Next: NEXT = None,
        End: END = None,
        InputPath: PATH_INPUT = None,
        OutputPath: PATH_INPUT = None,
        ResultPath: PATH_INPUT = None,
        Catch: CATCH = None,
        Retry: RETRY = None,
        TimeoutSeconds: TIMEOUT_SECONDS = None,
        HeartbeatSeconds: HEARTBEAT_SECONDS = None,
        JobDefinition: Optional[Any] = None,
        JobName: Optional[str] = None,
        JobQueue: Optional[Any] = None,
        Parameters: Parameters = None,
        ArrayProperties: Optional[Any] = None,
        ContainerOverrides: Optional[Any] = None,
        DependsOn: Optional[Any] = None,
        RetryStrategy: Optional[Any] = None,
        Timeout: Optional[Any] = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
    ): ...
    JobDefinition: Optional[Any]
    JobName: Optional[str]
    JobQueue: Optional[Any]
    Parameters: Parameters
    ArrayProperties: Optional[Any]
    ContainerOverrides: Optional[Any]
    DependsOn: Optional[Any]
    RetryStrategy: Optional[Any]
    Timeout: Optional[Any]
    Pattern: IntegrationPattern
