from typing import Any, Optional

from rhodes._types import CATCH, COMMENT, END, HEARTBEAT_SECONDS, NEXT, PATH_INPUT, RETRY, TIMEOUT_SECONDS, TITLE
from rhodes.identifiers import IntegrationPattern
from rhodes.states.services import ServiceIntegration

class AmazonSns(ServiceIntegration):
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
        Message: Optional[Any] = None,
        MessageAttributes: Optional[Any] = None,
        MessageStructure: Optional[Any] = None,
        Subject: Optional[Any] = None,
        PhoneNumber: Optional[Any] = None,
        TargetArn: Optional[Any] = None,
        TopicArn: Optional[Any] = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
    ): ...
    Message: Optional[Any]
    MessageAttributes: Optional[Any]
    MessageStructure: Optional[Any]
    Subject: Optional[Any]
    PhoneNumber: Optional[Any]
    TargetArn: Optional[Any]
    TopicArn: Optional[Any]
    Pattern: IntegrationPattern
