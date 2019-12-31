"""
`Amazon SQS <https://docs.aws.amazon.com/step-functions/latest/dg/connect-sqs.html>`_ Task state.
"""
import attr

from rhodes._util import RHODES_ATTRIB, RequiredValue
from rhodes.identifiers import IntegrationPattern, ServiceArn
from rhodes.states import State
from rhodes.states.services._util import service_integration

__all__ = ("AmazonSqs",)


@attr.s(eq=False)
@service_integration(IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.WAIT_FOR_CALLBACK)
class AmazonSqs(State):
    """
    :param DelaySeconds: The length of time, in seconds, for which to delay a specific message.
       Valid values: 0 to 900. Maximum: 15 minutes.
    :param MessageAttribute: Each message attribute consists of a Name, Type, and Value.
    :param MessageBody: The message to send. The maximum string size is 256 KB.
    :param MessageDeduplicationId: The token used for deduplication of sent messages.
    :param MessageGroupId: The tag that specifies that a message belongs to a specific message group.
    :param QueueUrl: The URL of the Amazon SQS queue to which a message is sent.
    """

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
