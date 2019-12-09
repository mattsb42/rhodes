from typing import Optional

from rhodes._types import CATCH, COMMENT, END, HEARTBEAT_SECONDS, NEXT, PATH_INPUT, RETRY, TIMEOUT_SECONDS, TITLE
from rhodes.identifiers import IntegrationPattern
from rhodes.states.services import ServiceIntegration
from rhodes.structures import JsonPath, Parameters

AWS_LAMBDA_DEFAULT_INVOCATION_TYPE: str

class AwsLambda(ServiceIntegration):
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
        FunctionName: Optional[str] = None,
        Payload: Optional[Parameters] = None,
        ClientContext: Optional[str] = None,
        InvocationType: Optional[str] = AWS_LAMBDA_DEFAULT_INVOCATION_TYPE,
        Qualifier: Optional[str] = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
    ): ...
    FunctionName: Optional[str]
    Payload: Optional[Parameters]
    ClientContext: Optional[str]
    InvocationType: Optional[str]
    Qualifier: Optional[str]
    Pattern: IntegrationPattern
