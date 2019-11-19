"""AWS Lambda Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/connect-lambda.html
"""
import attr
from attr.validators import in_

from rhodes._util import RequiredValue
from rhodes.states.services import IntegrationPattern, ServiceArn, ServiceIntegration, _supports_patterns

__all__ = ("AwsLambda",)

AWS_LAMBDA_DEFAULT_INVOCATION_TYPE = "RequestResponse"
AWS_LAMBDA_INVOCATION_TYPES = ("Event", AWS_LAMBDA_DEFAULT_INVOCATION_TYPE, "DryRun")


@attr.s(eq=False)
@_supports_patterns(IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.WAIT_FOR_CALLBACK)
class AwsLambda(ServiceIntegration):
    _required_fields = (RequiredValue("FunctionName", "AWS Lambda Task requires a function name."),)
    _resource_name = ServiceArn.AWSLAMBDA

    # TODO: FunctionName MUST have length 1 <= n <= 170
    #  Pattern: (arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_\.]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?
    FunctionName = attr.ib(default=None)
    # TODO: Determine validation for Payload
    #  Payload can also de-reference...how many layers deep?
    Payload = attr.ib(default=None)
    # TODO: ClientContext MUST have length n <= 3583
    ClientContext = attr.ib(default=None)
    InvocationType = attr.ib(default=AWS_LAMBDA_DEFAULT_INVOCATION_TYPE, validator=in_(AWS_LAMBDA_INVOCATION_TYPES))
    # TODO: Qualifier MUST have length 1 <= n <= 128
    Qualifier = attr.ib(default=None)
