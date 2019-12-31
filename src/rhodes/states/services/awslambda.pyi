from typing import Optional, Union

from rhodes._types import (
    AWS_LAMBDA_FUNCTION,
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
from rhodes.structures import JsonPath

AWS_LAMBDA_DEFAULT_INVOCATION_TYPE: str

class AwsLambda(State):
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
        FunctionName: Optional[SERVICE_INTEGRATION_SIMPLE_VALUE] = None,
        Payload: Optional[SERVICE_INTEGRATION_COMPLEX_VALUE] = None,
        ClientContext: Optional[SERVICE_INTEGRATION_SIMPLE_VALUE] = None,
        InvocationType: SERVICE_INTEGRATION_SIMPLE_VALUE = AWS_LAMBDA_DEFAULT_INVOCATION_TYPE,
        Qualifier: Optional[SERVICE_INTEGRATION_SIMPLE_VALUE] = None,
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
    FunctionName: Optional[AWS_LAMBDA_FUNCTION]
    Payload: Optional[Union[SERVICE_INTEGRATION_SIMPLE_VALUE, SERVICE_INTEGRATION_COMPLEX_VALUE]]
    ClientContext: Optional[SERVICE_INTEGRATION_SIMPLE_VALUE]
    InvocationType: SERVICE_INTEGRATION_SIMPLE_VALUE
    Qualifier: Optional[SERVICE_INTEGRATION_SIMPLE_VALUE]
    Pattern: IntegrationPattern
