"""
`Amazon SNS <https://docs.aws.amazon.com/step-functions/latest/dg/connect-sns.html>`_ Task state.
"""
from typing import Dict

import attr
from attr.validators import instance_of, optional

from rhodes._runtime_types import SERVICE_INTEGRATION_COMPLEX_VALUE_TYPES, SERVICE_INTEGRATION_SIMPLE_VALUE_TYPES
from rhodes._util import RHODES_ATTRIB, RequiredValue
from rhodes.identifiers import IntegrationPattern, ServiceArn
from rhodes.states import State
from rhodes.states.services._util import service_integration

__all__ = ("AmazonSns",)


@attr.s(eq=False)
@service_integration(IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.WAIT_FOR_CALLBACK)
class AmazonSns(State):
    """Send a message to target using Amazon SNS.
    Target can be an Amazon SNS topic,
    a text message (SMS message) directly to a phone number,
    or a message to a mobile platform endpoint (when you specify the TargetArn).

    `See service docs for more details.
    <https://docs.aws.amazon.com/sns/latest/api/API_Publish.html>`_

    Exactly one of ``PhoneNumber``, ``TargetArn``, or ``TopicArn`` must be provided.

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

    Message = RHODES_ATTRIB(validator=optional(instance_of(SERVICE_INTEGRATION_SIMPLE_VALUE_TYPES)))
    MessageAttributes = RHODES_ATTRIB(validator=optional(instance_of(SERVICE_INTEGRATION_COMPLEX_VALUE_TYPES)))
    MessageStructure = RHODES_ATTRIB(validator=optional(instance_of(SERVICE_INTEGRATION_SIMPLE_VALUE_TYPES)))
    Subject = RHODES_ATTRIB(validator=optional(instance_of(SERVICE_INTEGRATION_SIMPLE_VALUE_TYPES)))
    PhoneNumber = RHODES_ATTRIB(validator=optional(instance_of(SERVICE_INTEGRATION_SIMPLE_VALUE_TYPES)))
    TargetArn = RHODES_ATTRIB(validator=optional(instance_of(SERVICE_INTEGRATION_SIMPLE_VALUE_TYPES)))
    TopicArn = RHODES_ATTRIB(validator=optional(instance_of(SERVICE_INTEGRATION_SIMPLE_VALUE_TYPES)))

    @Message.validator
    def _validate_message(self, attribute, value):
        # pylint: disable=no-self-use,unused-argument
        if not isinstance(value, str):
            return

        # TODO: If MessageStructure == 'json', validate that message body is JSON.
        #  ...does that mean dictionary or JSON-encoded string?

    @MessageStructure.validator
    def _validate_message_structure(self, attribute, value):
        # pylint: disable=no-self-use,unused-argument
        if not isinstance(value, str):
            return

        if value != "json":
            raise ValueError("If MessageStructure is provided, it must be 'json'.")

    @Subject.validator
    def _validate_subject(self, attribute, value):
        # pylint: disable=no-self-use,unused-argument
        if not isinstance(value, str):
            return

        max_length = 100

        if not self.Subject:
            raise ValueError("Subject must not be empty.")

        # TODO:
        #  Constraints: Subjects must be ASCII text that begins with
        #  a letter, number, or punctuation mark;
        #  must not include line breaks or control characters;
        #  and must be less than 100 characters long.
        #  QUESTION: What exactly constitutes a "punctuation mark"?

        if len(self.Subject) > max_length:
            raise ValueError(f"Subject length must not exceed {max_length} characters. Received {len(self.Subject)}.")

    def _enforce_exactly_one_target(self):
        targets_set = sum((1 for target in (self.PhoneNumber, self.TargetArn, self.TopicArn) if target is not None))

        if targets_set != 1:
            raise ValueError("Exactly one of PhoneNumber, TargetArn, or TopicArn must be provided.")

    def __attrs_post_init__(self):
        self._enforce_exactly_one_target()

    def to_dict(self) -> Dict:
        self._enforce_exactly_one_target()

        return super(AmazonSns, self).to_dict()
