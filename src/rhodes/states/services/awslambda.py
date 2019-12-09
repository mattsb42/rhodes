"""AWS Lambda Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/connect-lambda.html
"""
import attr
from attr.validators import in_, instance_of, optional

from rhodes._util import RHODES_ATTRIB, RequiredValue
from rhodes.identifiers import IntegrationPattern, ServiceArn
from rhodes.states.services import ServiceIntegration
from rhodes.states.services.util import supports_patterns
from rhodes.structures import Parameters

__all__ = ("AwsLambda",)

AWS_LAMBDA_DEFAULT_INVOCATION_TYPE = "RequestResponse"
AWS_LAMBDA_INVOCATION_TYPES = ("Event", AWS_LAMBDA_DEFAULT_INVOCATION_TYPE, "DryRun")


@attr.s(eq=False)
@supports_patterns(IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.WAIT_FOR_CALLBACK)
class AwsLambda(ServiceIntegration):
    _required_fields = (RequiredValue("FunctionName", "AWS Lambda Task requires a function name."),)
    _resource_name = ServiceArn.AWSLAMBDA

    # TODO: FunctionName MUST have length 1 <= n <= 170
    #  Pattern: (arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_\.]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?
    FunctionName = RHODES_ATTRIB()
    Payload = RHODES_ATTRIB(validator=optional(instance_of(Parameters)))
    ClientContext = RHODES_ATTRIB(validator=optional(instance_of(str)))
    InvocationType = RHODES_ATTRIB(
        default=AWS_LAMBDA_DEFAULT_INVOCATION_TYPE, validator=in_(AWS_LAMBDA_INVOCATION_TYPES)
    )
    Qualifier = RHODES_ATTRIB(validator=optional(instance_of(str)))

    @ClientContext.validator
    def _validate_clientcontext(self, attribute, value):
        if value is None:
            return

        max_length = 3583
        actual = len(value)
        if actual > max_length:
            raise ValueError(f"'ClientContext' length {actual} is larger than maximum {max_length}.")

    @Qualifier.validator
    def _validate_qualifier(self, attribute, value):
        if value is None:
            return

        min_length = 1
        max_length = 128
        actual = len(value)
        if not min_length <= actual <= max_length:
            raise ValueError(
                f"'ClientContext' length {actual} is outside allowed range from {min_length} to {max_length}."
            )
