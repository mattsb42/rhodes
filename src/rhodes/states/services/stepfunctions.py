"""AWS Step Functions Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/connect-stepfunctions.html
"""
import attr
from attr.validators import instance_of, optional

from rhodes._runtime_types import SERVICE_INTEGRATION_COMPLEX_VALUE_TYPES, SERVICE_INTEGRATION_SIMPLE_VALUE_TYPES
from rhodes._util import RHODES_ATTRIB, RequiredValue
from rhodes.identifiers import IntegrationPattern, ServiceArn
from rhodes.states.services import ServiceIntegration
from rhodes.states.services.util import supports_patterns
from rhodes.structures import Parameters


@attr.s(eq=False)
@supports_patterns(
    IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.SYNCHRONOUS, IntegrationPattern.WAIT_FOR_CALLBACK
)
class AwsStepFunctions(ServiceIntegration):
    _required_fields = (RequiredValue("StateMachineArn", "AWS Step Functions Task requires a state machine target"),)
    _resource_name = ServiceArn.STEP_FUNCTIONS

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html#API_StartExecution_RequestSyntax

    StateMachineArn = RHODES_ATTRIB(validator=optional(instance_of(SERVICE_INTEGRATION_SIMPLE_VALUE_TYPES)))
    # SFn docs say that this needs to be a string,
    #  but in practice JSON can be provided inline in the state machine
    Input = RHODES_ATTRIB(validator=optional(instance_of(SERVICE_INTEGRATION_COMPLEX_VALUE_TYPES)))
    # TODO: I'm inclined to say that either Name is not acceptable or that it MUST be a JsonPath.
    #  Leaving this alone until I can decide one way or the other.
    # Name = RHODES_ATTRIB()
