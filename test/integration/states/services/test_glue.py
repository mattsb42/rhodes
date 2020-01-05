"""Integration tests for ``rhodes.states.services.glue``."""
import pytest

from rhodes.states.services.glue import AwsGlue
from rhodes.structures import Parameters

from ...integration_test_utils import build_and_try_single_step_state_machine

pytestmark = [pytest.mark.integ]


def test_glue_minimal():
    step = AwsGlue("test", JobName="foo")
    build_and_try_single_step_state_machine(step)


def test_glue_all_specials():
    step = AwsGlue(
        "test",
        JobName="foo",
        JobRunId="bar",
        Arguments=Parameters(foo="bar"),
        AllocatedCapacity=12,
        Timeout=7,
        SecurityConfiguration="foo",
        NotificationProperty=Parameters(NotifyDelayAfter=8),
    )
    build_and_try_single_step_state_machine(step)
