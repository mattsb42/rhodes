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
    """Submit an AWS Batch job from a job definition.

    `See service docs for more details.
    <https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html>`_

    :param JobDefinition: The job definition used by this job.
      This value can be one of name, name:revision, or the Amazon Resource Name (ARN) for the job definition.
      If name is specified without a revision then the latest active revision is used.
    :param JobName: The name of the job.
      The first character must be alphanumeric,
      and up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.
    :param JobQueue: The job queue into which the job is submitted.
      You can specify either the name or the Amazon Resource Name (ARN) of the queue.
    :param Parameters: Additional parameters passed to the job.
       These replace parameter substitution placeholders that are set in the job definition.
       Parameters are specified as a key and value pair mapping.
       Parameters in a SubmitJob request override any corresponding parameter defaults from the job definition.
    :param ArrayProperties: The array properties for the submitted job, such as the size of the array.
      The array size can be between 2 and 10,000.
      If you specify array properties for a job, it becomes an array job.
    :param ContainerOverrides: A list of container overrides in JSON format.
      These specify the name of a container in the specified job definition and the overrides it should receive.
      You can override the default command for a container with a command override.
      You can also override existing environment variables on a container
      or add new environment variables to it with an environment override.
    :param DependsOn: A list of dependencies for the job.
      A job can depend upon a maximum of 20 jobs.
    :param RetryStrategy: The retry strategy to use for failed jobs from this SubmitJob operation.
      When a retry strategy is specified here, it overrides the retry strategy defined in the job definition.
    :param Timeout: The timeout configuration for this SubmitJob operation.
      If a job is terminated due to a timeout, it is not retried.
      The minimum value for the timeout is 60 seconds.
      This configuration overrides any timeout configuration specified in the job definition.
      For array jobs, child jobs have the same timeout configuration as the parent job.
    """

    _required_fields = (
        RequiredValue("JobDefinition", "AWS Batch Task requires a job definition."),
        RequiredValue("JobName", "AWS Batch Task requires a job name."),
        RequiredValue("JobQueue", "AWS Batch Task requires a job queue."),
    )
    _resource_name = ServiceArn.BATCH

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html#Batch-SubmitJob-request-arrayProperties

    # TODO: A lot of these accept structured data.
    #  It would appear that despite what the underlying service APIs have to say,
    #  Step Functions requires LITERALLY EVERYTHING
    #  that might be a predictable structure to be in PascalCase.

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
