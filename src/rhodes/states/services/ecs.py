"""Amazon ECS/Fargate Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/connect-ecs.html
"""
import attr

from rhodes._util import RHODES_ATTRIB, RequiredValue
from rhodes.states.services import ServiceIntegration
from rhodes.states.services.identifiers import IntegrationPattern, ServiceArn
from rhodes.states.services.util import supports_patterns


@attr.s(eq=False)
@supports_patterns(
    IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.SYNCHRONOUS, IntegrationPattern.WAIT_FOR_CALLBACK
)
class AmazonEcs(ServiceIntegration):
    _required_fields = (RequiredValue("TaskDefinition", "Amazon ECS Task requires a task definition"),)
    _resource_name = ServiceArn.ECS

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html#ECS-RunTask-request-cluster

    Cluster = RHODES_ATTRIB()
    Group = RHODES_ATTRIB()
    LaunchType = RHODES_ATTRIB()
    NetworkConfiguration = RHODES_ATTRIB()
    Overrides = RHODES_ATTRIB()
    PlacementConstraints = RHODES_ATTRIB()
    PlacementStrategy = RHODES_ATTRIB()
    PlatformVersion = RHODES_ATTRIB()
    TaskDefinition = RHODES_ATTRIB()
