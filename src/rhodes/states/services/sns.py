"""Amazon SNS Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/connect-sns.html
"""
import attr

from rhodes._util import RequiredValue
from rhodes.states.services import IntegrationPattern, ServiceArn, ServiceIntegration, _supports_patterns


@attr.s(eq=False)
@_supports_patterns(IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.WAIT_FOR_CALLBACK)
class AmazonSns(ServiceIntegration):
    _required_fields = (RequiredValue("Message", "Amazon SNS Task requires a message"),)
    _resource_name = ServiceArn.SNS

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sns/latest/api/API_Publish.html#API_Publish_RequestParameters

    Message = attr.ib(default=None)
    MessageAttributes = attr.ib(default=None)
    MessageStructure = attr.ib(default=None)
    Subject = attr.ib(default=None)
    # one of the below is required
    PhoneNumber = attr.ib(default=None)
    TargetArn = attr.ib(default=None)
    TopicArn = attr.ib(default=None)
