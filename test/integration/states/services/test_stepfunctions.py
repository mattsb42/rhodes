"""Integration tests for ``rhodes.states.services.stepfunctions``."""
import pytest

from rhodes.states.services.stepfunctions import AwsStepFunctions

from ...integration_test_utils import (
    SERVICE_INTEGRATION_BOTH_CASES,
    SERVICE_INTEGRATION_SIMPLE_CASES,
    build_and_try_single_step_state_machine,
)

pytestmark = [pytest.mark.integ]


@pytest.mark.parametrize("state_machine_arn", SERVICE_INTEGRATION_SIMPLE_CASES[1:])
@pytest.mark.parametrize("state_machine_input", SERVICE_INTEGRATION_BOTH_CASES)
def test_stepfunctions(state_machine_arn, state_machine_input):
    step = AwsStepFunctions("test", StateMachineArn=state_machine_arn, Input=state_machine_input)
    build_and_try_single_step_state_machine(step)
