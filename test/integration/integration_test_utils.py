"""Helper utilities for integration tests."""
import json
from datetime import datetime, timezone
from enum import Enum
from functools import lru_cache
from uuid import uuid4

import boto3

from rhodes.states import StateMachine
from rhodes.structures import JsonPath, Parameters

__all__ = (
    "try_to_create_and_delete_state_machine",
    "build_and_try_single_step_state_machine",
    "SERVICE_INTEGRATION_SIMPLE_CASES",
    "SERVICE_INTEGRATION_COMPLEX_CASES",
    "SERVICE_INTEGRATION_BOTH_CASES",
)


class JunkEnum(Enum):
    FOO = "BAR"


SERVICE_INTEGRATION_SIMPLE_CASES = (None, "some data", JunkEnum.FOO, JsonPath("$.foo.bar"))
SERVICE_INTEGRATION_COMPLEX_CASES = (
    None,
    JsonPath("$.foo.bar"),
    JunkEnum.FOO,
    Parameters(foo="bar"),
    dict(foo="bar"),
)
SERVICE_INTEGRATION_BOTH_CASES = SERVICE_INTEGRATION_SIMPLE_CASES + SERVICE_INTEGRATION_COMPLEX_CASES[3:]


def _state_machine_name() -> str:
    return f"rhodes-integ-{uuid4()}"


@lru_cache(maxsize=1)
def _role_arn() -> str:
    """Generate a dummy role ARN.
    The only thing that Step Functions validates at state machine creation time
    is that the role ARN is well formed.
    IAM also only allows passing roles within an account,
    which is why we need to get the current account ID from STS.

    Only doing this once saves ~400ms per test.
    Given how many tests we're running, this adds up FAST.
    """
    sts = boto3.client("sts")
    account_id = sts.get_caller_identity()["Account"]
    return f"arn:aws:iam::{account_id}:role/{uuid4()}"


@lru_cache(maxsize=1)
def _sfn_client():
    """Only create the Step Functions client once.
    This saves ~500ms per test.
    Given how many tests we're running, this adds up FAST.
    """
    return boto3.client("stepfunctions")


def create_state_machine(state_machine_definition: str):
    sfn = _sfn_client()
    response = sfn.create_state_machine(
        name=_state_machine_name(),
        roleArn=_role_arn(),
        definition=state_machine_definition,
        tags=[
            dict(key="rhodes", value="integration test"),
            dict(key="creation time", value=datetime.now(timezone.utc).isoformat()),
        ],
    )

    return response["stateMachineArn"]


def delete_state_machine(state_machine_arn: str):
    sfn = _sfn_client()
    sfn.delete_state_machine(stateMachineArn=state_machine_arn)


def try_to_create_and_delete_state_machine(state_machine_definition: str):
    state_machine_arn = create_state_machine(state_machine_definition)
    delete_state_machine(state_machine_arn)


def build_and_try_single_step_state_machine(step):
    workflow = StateMachine()
    workflow.start_with(step).end()

    definition = json.dumps(workflow.to_dict())
    try_to_create_and_delete_state_machine(definition)
