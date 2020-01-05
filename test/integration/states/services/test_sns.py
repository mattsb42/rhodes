"""Integration tests for ``rhodes.states.services.sns``."""
import pytest

from rhodes.states.services.sns import AmazonSns

from ...integration_test_utils import build_and_try_single_step_state_machine

pytestmark = [pytest.mark.integ]


@pytest.mark.parametrize("target", (dict(PhoneNumber="123"), dict(TargetArn="foo"), dict(TopicArn="bar"),))
def test_sns_minimal(target):
    step = AmazonSns("test", Message="foo bar baz", **target)
    build_and_try_single_step_state_machine(step)


@pytest.mark.parametrize("target", (dict(PhoneNumber="123"), dict(TargetArn="foo"), dict(TopicArn="bar"),))
def test_sns_all_special(target):
    step = AmazonSns(
        "test",
        Message="foo bar baz",
        # TODO: I don't really understand what these message attributes things are...
        #  MessageAttributes="??",
        MessageStructure="json",
        Subject="zab rab oof",
        **target,
    )
    build_and_try_single_step_state_machine(step)
