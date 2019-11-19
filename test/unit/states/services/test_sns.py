"""Unit test suite for ``rhodes.states.services.sns``."""
import pytest

from rhodes.states import Parameters, Task
from rhodes.states.services import IntegrationPattern
from rhodes.states.services.sns import AmazonSns
from rhodes.structures import JsonPath

pytestmark = [pytest.mark.local, pytest.mark.functional]


def test_amazon_sns_request_response():
    expected_task = Task(
        "TestTask",
        Resource="arn:aws:states:::sns:publish",
        Parameters=Parameters(
            TopicArn="arn:aws:sns:us-east-1:123456789012:accretion-notify", Message=JsonPath("$.foo.bar")
        ),
    )
    expected = expected_task.to_dict()

    test_task = AmazonSns(
        "TestTask", TopicArn="arn:aws:sns:us-east-1:123456789012:accretion-notify", Message=JsonPath("$.foo.bar")
    )
    test = test_task.to_dict()

    assert test == expected


def test_amazon_sns_callback():
    expected_task = Task(
        "TestTask",
        Resource="arn:aws:states:::sns:publish.waitForTaskToken",
        Parameters=Parameters(
            TopicArn="arn:aws:sns:us-east-1:123456789012:accretion-notify", Message=JsonPath("$.foo.bar")
        ),
    )
    expected = expected_task.to_dict()

    test_task = AmazonSns(
        "TestTask",
        Pattern=IntegrationPattern.WAIT_FOR_CALLBACK,
        TopicArn="arn:aws:sns:us-east-1:123456789012:accretion-notify",
        Message=JsonPath("$.foo.bar"),
    )
    test = test_task.to_dict()

    assert test == expected
