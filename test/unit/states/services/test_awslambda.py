"""Unit test suite for ``rhodes.states.services.awslambda``."""
import pytest

from rhodes.states import Parameters, Task
from rhodes.states.services import IntegrationPattern
from rhodes.states.services.awslambda import AwsLambda
from rhodes.structures import JsonPath

pytestmark = [pytest.mark.local, pytest.mark.functional]


def test_aws_lambda_request_response():
    expected_task = Task(
        "TestTask",
        Resource="arn:aws:states:::lambda:invoke",
        Parameters=Parameters(
            FunctionName="arn:aws:lambda:us-east-1:123456789012:function:ship-val",
            Payload={"test": "value"},
            InvocationType="RequestResponse",
        ),
    )
    expected = expected_task.to_dict()

    test_task = AwsLambda(
        "TestTask", FunctionName="arn:aws:lambda:us-east-1:123456789012:function:ship-val", Payload={"test": "value"}
    )
    test = test_task.to_dict()

    assert test == expected


def test_aws_lambda_callback():
    expected_task = Task(
        "TestTask",
        Resource="arn:aws:states:::lambda:invoke.waitForTaskToken",
        Parameters=Parameters(
            FunctionName="arn:aws:lambda:us-east-1:123456789012:function:ship-val",
            Payload={"test": "value"},
            InvocationType="RequestResponse",
        ),
    )
    expected = expected_task.to_dict()

    test_task = AwsLambda(
        "TestTask",
        Pattern=IntegrationPattern.WAIT_FOR_CALLBACK,
        FunctionName="arn:aws:lambda:us-east-1:123456789012:function:ship-val",
        Payload={"test": "value"},
    )
    test = test_task.to_dict()

    assert test == expected
