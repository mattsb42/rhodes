"""Amazon SQS Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/connect-sqs.html
"""
import attr

from rhodes._util import RHODES_ATTRIB, RequiredValue
from rhodes.identifiers import IntegrationPattern, ServiceArn
from rhodes.states.services import ServiceIntegration
from rhodes.states.services.util import supports_patterns


@attr.s(eq=False)
@supports_patterns(IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.WAIT_FOR_CALLBACK)
class AmazonSqs(ServiceIntegration):
    _required_fields = (
        RequiredValue("MessageBody", "Amazon SQS Task requires a message body"),
        RequiredValue("QueueUrl", "Amazon SQS Task requires a queue url"),
    )
    _resource_name = ServiceArn.SQS

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/step-functions/latest/dg/connect-sqs.html

    DelaySeconds = RHODES_ATTRIB()
    MessageAttribute = RHODES_ATTRIB()
    MessageBody = RHODES_ATTRIB()
    MessageDeduplicationId = RHODES_ATTRIB()
    MessageGroupId = RHODES_ATTRIB()
    QueueUrl = RHODES_ATTRIB()
