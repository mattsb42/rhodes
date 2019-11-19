"""AWS Batch Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/connect-batch.html
"""
from typing import Dict, Iterable

import attr
from attr.validators import deep_mapping, instance_of

from rhodes._util import RequiredValue
from rhodes.states.services import IntegrationPattern, ServiceArn, ServiceIntegration, _supports_patterns

__all__ = ("AwsBatch",)


@attr.s(eq=False)
@_supports_patterns(IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.SYNCHRONOUS)
class AwsBatch(ServiceIntegration):
    _required_fields = (
        RequiredValue("JobDefinition", "AWS Batch Task requires a job definition."),
        RequiredValue("JobName", "AWS Batch Task requires a job name."),
        RequiredValue("JobQueue", "AWS Batch Task requires a job queue."),
    )
    _resource_name = ServiceArn.BATCH

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html#Batch-SubmitJob-request-arrayProperties

    # The ARN/name
    JobDefinition = attr.ib(default=None)
    # unique name...does SFn actually require this?
    JobName: str = attr.ib(default=None, validator=instance_of(str))
    # ??? ARN for something?
    JobQueue = attr.ib(default=None)
    # Arbitrary string-string map
    Parameters: Dict[str, str] = attr.ib(
        default=attr.Factory(dict),
        validator=deep_mapping(key_validator=instance_of(str), value_validator=instance_of(str)),
    )
    # TODO: These others feel like things that should already exist in Troposphere
    ArrayProperties: Iterable = attr.ib(default=None)
    ContainerOverrides = attr.ib(default=None)
    DependsOn = attr.ib(default=None)
    RetryStrategy = attr.ib(default=None)
    Timeout = attr.ib(default=None)
