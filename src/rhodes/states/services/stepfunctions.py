"""AWS Step Functions Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/connect-stepfunctions.html
"""
import attr

from rhodes._util import RequiredValue
from rhodes.states.services import IntegrationPattern, ServiceArn, ServiceIntegration, _supports_patterns


@attr.s(eq=False)
@_supports_patterns(
    IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.SYNCHRONOUS, IntegrationPattern.WAIT_FOR_CALLBACK
)
class AwsStepFunctions(ServiceIntegration):
    _required_fields = (RequiredValue("stateMachineArn", "AWS Step Functions Task requires a state machine target"),)
    _resource_name = ServiceArn.STEP_FUNCTIONS

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html#API_StartExecution_RequestSyntax

    # SFn docs say that this needs to be a string,
    #  but in practice JSON can be provided inline in the state machine
    input = attr.ib(default=None)
    name = attr.ib(default=None)
    stateMachineArn = attr.ib(default=None)
