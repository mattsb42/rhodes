"""Amazon SNS Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/connect-sns.html
"""
import attr

from rhodes._util import RHODES_ATTRIB, RequiredValue
from rhodes.identifiers import IntegrationPattern, ServiceArn
from rhodes.states.services import ServiceIntegration
from rhodes.states.services.util import supports_patterns


@attr.s(eq=False)
@supports_patterns(IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.WAIT_FOR_CALLBACK)
class AmazonSns(ServiceIntegration):
    _required_fields = (RequiredValue("Message", "Amazon SNS Task requires a message"),)
    _resource_name = ServiceArn.SNS

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sns/latest/api/API_Publish.html#API_Publish_RequestParameters

    Message = RHODES_ATTRIB()
    MessageAttributes = RHODES_ATTRIB()
    MessageStructure = RHODES_ATTRIB()
    Subject = RHODES_ATTRIB()
    # TODO:
    #  exactly one of the below is required
    PhoneNumber = RHODES_ATTRIB()
    TargetArn = RHODES_ATTRIB()
    TopicArn = RHODES_ATTRIB()
