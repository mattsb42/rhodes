"""Integration tests for ``rhodes.states.services.ecs``."""
import pytest

from rhodes.states.services.ecs import AmazonEcs
from rhodes.structures import Parameters

from ...integration_test_utils import build_and_try_single_step_state_machine

pytestmark = [pytest.mark.integ]


def test_ecs_minimal():
    step = AmazonEcs("test", TaskDefinition="bar")
    build_and_try_single_step_state_machine(step)


def test_ecs_all_specials():
    step = AmazonEcs(
        "test",
        Cluster="foo",
        Group="bar",
        LaunchType="baz",
        NetworkConfiguration=Parameters(AwsvpcConfiguration=Parameters(AssignPublicIp="wat")),
        Overrides=Parameters(ContainerOverrides=[dict(Cpu=3)]),
        PlacementConstraints=[dict(Expression="foo", Type="bar")],
        PlacementStrategy=[dict(Field="foo", Type="bar")],
        PlatformVersion="foo",
        TaskDefinition="bar",
    )
    build_and_try_single_step_state_machine(step)
