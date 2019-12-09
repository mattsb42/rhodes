from typing import Any, Optional

from rhodes._types import CATCH, COMMENT, END, HEARTBEAT_SECONDS, NEXT, PATH_INPUT, RETRY, TIMEOUT_SECONDS, TITLE
from rhodes.identifiers import IntegrationPattern
from rhodes.states.services import ServiceIntegration
from rhodes.structures import Parameters

class AwsStepFunctions(ServiceIntegration):
    def __init__(
        self,
        *,
        title: TITLE,
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
        StateMachineArn: Optional[Any] = None,
        Input: Optional[Parameters] = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
    ): ...
    StateMachineArn: Optional[Any]
    Input: Optional[Parameters]
    Pattern: IntegrationPattern
