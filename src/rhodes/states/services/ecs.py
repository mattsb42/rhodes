"""Amazon ECS/Fargate Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/connect-ecs.html
"""
import attr

from rhodes._util import RequiredValue
from rhodes.states.services import IntegrationPattern, ServiceArn, ServiceIntegration, _supports_patterns


@attr.s(eq=False)
@_supports_patterns(
    IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.SYNCHRONOUS, IntegrationPattern.WAIT_FOR_CALLBACK
)
class AmazonEcs(ServiceIntegration):
    _required_fields = (RequiredValue("TaskDefinition", "Amazon ECS Task requires a task definition"),)
    _resource_name = ServiceArn.ECS

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html#ECS-RunTask-request-cluster

    Cluster = attr.ib(default=None)
    Group = attr.ib(default=None)
    LaunchType = attr.ib(default=None)
    NetworkConfiguration = attr.ib(default=None)
    Overrides = attr.ib(default=None)
    PlacementConstraints = attr.ib(default=None)
    PlacementStrategy = attr.ib(default=None)
    PlatformVersion = attr.ib(default=None)
    TaskDefinition = attr.ib(default=None)
