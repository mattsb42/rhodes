from typing import Any, Optional

from rhodes._types import CATCH, COMMENT, END, HEARTBEAT_SECONDS, NEXT, PATH_INPUT, RETRY, TIMEOUT_SECONDS, TITLE
from rhodes.identifiers import IntegrationPattern
from rhodes.states.services import ServiceIntegration

class AwsGlue(ServiceIntegration):
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
        FunctionName: Optional[str] = None,
        JobName: Optional[Any] = None,
        JobRunId: Optional[Any] = None,
        Arguments: Optional[Any] = None,
        AllocatedCapacity: Optional[Any] = None,
        Timeout: Optional[Any] = None,
        SecurityConfiguration: Optional[Any] = None,
        NotificationProperty: Optional[Any] = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
    ): ...
    JobName: Optional[Any]
    JobRunId: Optional[Any]
    Arguments: Optional[Any]
    AllocatedCapacity: Optional[Any]
    Timeout: Optional[Any]
    SecurityConfiguration: Optional[Any]
    NotificationProperty: Optional[Any]
    Pattern: IntegrationPattern
