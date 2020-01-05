"""Integration tests for ``rhodes.states.services.awslambda``."""
import pytest

from rhodes.states.services.awslambda import AwsLambda

from ...integration_test_utils import (
    SERVICE_INTEGRATION_BOTH_CASES,
    SERVICE_INTEGRATION_SIMPLE_CASES,
    build_and_try_single_step_state_machine,
)

pytestmark = [pytest.mark.integ]


@pytest.mark.parametrize("payload", SERVICE_INTEGRATION_BOTH_CASES)
@pytest.mark.parametrize("client_context", SERVICE_INTEGRATION_SIMPLE_CASES)
@pytest.mark.parametrize("qualifier", SERVICE_INTEGRATION_SIMPLE_CASES)
def test_awslambda(payload, client_context, qualifier):
    step = AwsLambda("test", FunctionName="foo", Payload=payload, ClientContext=client_context, Qualifier=qualifier)
    build_and_try_single_step_state_machine(step)
