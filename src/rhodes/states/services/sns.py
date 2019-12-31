"""
`Amazon SNS <https://docs.aws.amazon.com/step-functions/latest/dg/connect-sns.html>`_ Task state.
"""
import attr

from rhodes._util import RHODES_ATTRIB, RequiredValue
from rhodes.identifiers import IntegrationPattern, ServiceArn
from rhodes.states import State
from rhodes.states.services._util import service_integration

__all__ = ("AmazonSns",)


@attr.s(eq=False)
@service_integration(IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.WAIT_FOR_CALLBACK)
class AmazonSns(State):
    """
    :param Message: The message you want to send.
    :param MessageAttributes: Message attributes for Publish action.
    :param MessageStructure: Set MessageStructure to json if you want to send a different message for each protocol.
    :param Subject:
       Optional parameter to be used as the "Subject" line when the message is delivered to email endpoints.
       This field will also be included, if present, in the standard JSON messages delivered to other endpoints.
    :param PhoneNumber: The phone number to which you want to deliver an SMS message. Use E.164 format.
    :param TargetArn: If you don't specify a value for the TargetArn parameter,
       you must specify a value for the PhoneNumber or TopicArn parameters.
    :param TopicArn: The topic you want to publish to.
    """

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
