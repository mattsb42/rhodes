"""
`AWS Batch <https://docs.aws.amazon.com/step-functions/latest/dg/connect-batch.html>`_ Task state.
"""
import attr

from rhodes._util import RHODES_ATTRIB, RequiredValue
from rhodes.identifiers import IntegrationPattern, ServiceArn
from rhodes.states import State
from rhodes.states.services._util import service_integration
from rhodes.structures import Parameters

__all__ = ("AwsBatch",)


@attr.s(eq=False)
@service_integration(IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.SYNCHRONOUS)
class AwsBatch(State):
    """
    :param JobDefinition:
    :param JobName:
    :param JobQueue:
    :param Parameters:
    :param ArrayProperties:
    :param ContainerOverrides:
    :param DependsOn:
    :param RetryStrategy:
    :param Timeout:
    """

    _required_fields = (
        RequiredValue("JobDefinition", "AWS Batch Task requires a job definition."),
        RequiredValue("JobName", "AWS Batch Task requires a job name."),
        RequiredValue("JobQueue", "AWS Batch Task requires a job queue."),
    )
    _resource_name = ServiceArn.BATCH

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html#Batch-SubmitJob-request-arrayProperties

    # The ARN/name
    JobDefinition = RHODES_ATTRIB()
    # unique name...does SFn actually require this?
    JobName = RHODES_ATTRIB()
    # ??? ARN for something?
    JobQueue = RHODES_ATTRIB()
    Parameters: Parameters = RHODES_ATTRIB()
    # TODO: These others feel like things that should already exist in Troposphere
    ArrayProperties = RHODES_ATTRIB()
    ContainerOverrides = RHODES_ATTRIB()
    DependsOn = RHODES_ATTRIB()
    RetryStrategy = RHODES_ATTRIB()
    Timeout = RHODES_ATTRIB()
