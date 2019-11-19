"""Amazon SQS Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/connect-sqs.html
"""
import attr

from rhodes._util import RequiredValue
from rhodes.states.services import IntegrationPattern, ServiceArn, ServiceIntegration, _supports_patterns


@attr.s(eq=False)
@_supports_patterns(IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.WAIT_FOR_CALLBACK)
class AmazonSqs(ServiceIntegration):
    _required_fields = (
        RequiredValue("MessageBody", "Amazon SQS Task requires a message body"),
        RequiredValue("QueueUrl", "Amazon SQS Task requires a queue url"),
    )
    _resource_name = ServiceArn.SQS

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/step-functions/latest/dg/connect-sqs.html

    DelaySeconds = attr.ib(default=None)
    MessageAttribute = attr.ib(default=None)
    MessageBody = attr.ib(default=None)
    MessageDeduplicationId = attr.ib(default=None)
    MessageGroupId = attr.ib(default=None)
    QueueUrl = attr.ib(default=None)
