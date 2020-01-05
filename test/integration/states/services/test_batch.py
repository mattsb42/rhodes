"""Integration tests for ``rhodes.states.services.batch``."""
import pytest

from rhodes.states.services.batch import AwsBatch
from rhodes.structures import Parameters

from ...integration_test_utils import build_and_try_single_step_state_machine

pytestmark = [pytest.mark.integ]


def test_batch_minimal():
    step = AwsBatch("test", JobDefinition="foo", JobName="bar", JobQueue="foo")
    build_and_try_single_step_state_machine(step)


def test_batch_all_specials():
    step = AwsBatch(
        "test",
        JobDefinition="foo",
        JobName="bar",
        JobQueue="foo",
        Parameters=Parameters(foo="bar"),
        ArrayProperties=Parameters(Size=5),
        ContainerOverrides=Parameters(Memory=12),
        DependsOn=[dict(JobId="foo", Type="bar")],
        RetryStrategy=Parameters(Attempts=3),
        Timeout=Parameters(AttemptDurationSeconds=9),
    )
    build_and_try_single_step_state_machine(step)
