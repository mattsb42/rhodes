from typing import Any, Optional

from rhodes._types import CATCH, COMMENT, END, HEARTBEAT_SECONDS, NEXT, PATH_INPUT, RETRY, TIMEOUT_SECONDS, TITLE
from rhodes.identifiers import IntegrationPattern
from rhodes.states.services import ServiceIntegration
from rhodes.structures import JsonPath

AWS_LAMBDA_DEFAULT_INVOCATION_TYPE: str

class AmazonSqs(ServiceIntegration):
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
        DelaySeconds: Optional[Any] = None,
        MessageAttribute: Optional[Any] = None,
        MessageBody: Optional[Any] = None,
        MessageDeduplicationId: Optional[Any] = None,
        MessageGroupId: Optional[Any] = None,
        QueueUrl: Optional[Any] = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
    ): ...
    DelaySeconds: Optional[Any]
    MessageAttribute: Optional[Any]
    MessageBody: Optional[Any]
    MessageDeduplicationId: Optional[Any]
    MessageGroupId: Optional[Any]
    QueueUrl: Optional[Any]
    Pattern: IntegrationPattern
