"""
`Amazon ECS/Fargate <https://docs.aws.amazon.com/step-functions/latest/dg/connect-ecs.html>`_ Task state.
"""
import attr

from rhodes._util import RHODES_ATTRIB, RequiredValue
from rhodes.identifiers import IntegrationPattern, ServiceArn
from rhodes.states import State
from rhodes.states.services._util import service_integration

__all__ = ("AmazonEcs",)


@attr.s(eq=False)
@service_integration(
    IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.SYNCHRONOUS, IntegrationPattern.WAIT_FOR_CALLBACK
)
class AmazonEcs(State):
    """
    :param Cluster: The short name or full Amazon Resource Name (ARN) of the cluster on which to run your task.
       If you do not specify a cluster, the default cluster is assumed.
    :param Group: The name of the task group to associate with the task.
       The default value is the family name of the task definition (for example, family:my-family-name).
    :param LaunchType: The launch type on which to run your task.
       For more information, see Amazon ECS Launch Types in the Amazon Elastic Container Service Developer Guide.
    :param NetworkConfiguration: The network configuration for the task.
       This parameter is required for task definitions that use the awsvpc network mode
       to receive their own elastic network interface, and it is not supported for other network modes.
       For more information, see Task Networking in the Amazon Elastic Container Service Developer Guide.
    :param Overrides: A list of container overrides in JSON format that specify the name of a container
       in the specified task definition and the overrides it should receive.
    :param PlacementConstraints: An array of placement constraint objects to use for the task.
       You can specify up to 10 constraints per task
       (including constraints in the task definition and those specified at runtime).
    :param PlacementStrategy: The placement strategy objects to use for the task.
       You can specify a maximum of five strategy rules per task.
    :param PlatformVersion: The platform version the task should run.
       A platform version is only specified for tasks using the Fargate launch type.
       If one is not specified, the LATEST platform version is used by default.
       For more information, see AWS Fargate Platform Versions in the Amazon Elastic Container Service Developer Guide.
    :param TaskDefinition: The family and revision (family:revision) or full ARN of the task definition to run.
       If a revision is not specified, the latest ACTIVE revision is used.
    """

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
