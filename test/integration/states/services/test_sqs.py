"""Integration tests for ``rhodes.states.services.sqs``."""
import pytest

from rhodes.states.services.sqs import AmazonSqs

from ...integration_test_utils import build_and_try_single_step_state_machine

pytestmark = [pytest.mark.integ]


def test_sqs_minimal():
    step = AmazonSqs("test", MessageBody="foo bar baz", QueueUrl="omg",)
    build_and_try_single_step_state_machine(step)


def test_sqs_all_special():
    step = AmazonSqs(
        "test",
        DelaySeconds=123,
        # TODO: I don't really understand what these message attributes things are...
        #  MessageAttributes="??",
        MessageBody="foo bar baz",
        MessageDeduplicationId="wow",
        MessageGroupId="wat",
        QueueUrl="omg",
    )
    build_and_try_single_step_state_machine(step)
