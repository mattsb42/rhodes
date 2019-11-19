"""AWS Service Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/concepts-service-integrations.html
"""
from enum import Enum
from typing import Callable, Dict

import attr
from attr.validators import in_

from rhodes._util import require_field
from rhodes.states import Parameters, State, Task, task_type

__all__ = ("ServiceArn", "ServiceIntegration", "IntegrationPattern")

_DDB_BASE_ARN = "arn:aws:states:::dynamodb"
_SAGEMAKER_BASE_ARN = "arn:aws:states:::sagemaker"


class ServiceArn(Enum):
    AWSLAMBDA = "arn:aws:states:::lambda:invoke"
    BATCH = "arn:aws:states:::batch:submitJob"
    ECS = "arn:aws:states:::ecs:runTask"
    SNS = "arn:aws:states:::sns:publish"
    SQS = "arn:aws:states:::sqs:sendMessage"
    GLUE = "arn:aws:states:::glue:startJobRun"
    STEP_FUNCTIONS = "arn:aws:states:::states:startExecution"
    DYNAMODB_GET_ITEM = f"{_DDB_BASE_ARN}:getItem"
    DYNAMODB_PUT_ITEM = f"{_DDB_BASE_ARN}:putItem"
    DYNAMODB_DELETE_ITEM = f"{_DDB_BASE_ARN}:deleteItem"
    DYNAMODB_UPDATE_ITEM = f"{_DDB_BASE_ARN}:updateItem"
    SAGEMAKER_CREATE_ENDPOINT = f"{_SAGEMAKER_BASE_ARN}:createEndpoint"
    SAGEMAKER_CREATE_ENDPOINT_CONFIG = f"{_SAGEMAKER_BASE_ARN}:createEndpointConfig"
    SAGEMAKER_CREATE_HYPER_PARAMETER_TUNING_JOB = f"{_SAGEMAKER_BASE_ARN}:createHyperParameterTuningJob"
    SAGEMAKER_CREATE_LABELING_JOB = f"{_SAGEMAKER_BASE_ARN}:createLabelingJob"
    SAGEMAKER_CREATE_MODEL = f"{_SAGEMAKER_BASE_ARN}:createModel"
    SAGEMAKER_CREATE_TRAINING_JOB = f"{_SAGEMAKER_BASE_ARN}:createTrainingJob"
    SAGEMAKER_CREATE_TRANSFORM_JOB = f"{_SAGEMAKER_BASE_ARN}:createTransformJob"
    SAGEMAKER_UPDATE_ENDPOINT = f"{_SAGEMAKER_BASE_ARN}:updateEndpoint"


class IntegrationPattern(Enum):
    REQUEST_RESPONSE = ""
    SYNCHRONOUS = ".sync"
    WAIT_FOR_CALLBACK = ".waitForTaskToken"


@attr.s(eq=False)
@task_type
class ServiceIntegration(State):
    _resource_name = NotImplemented

    def to_task(self) -> Task:
        raise NotImplementedError()

    def to_dict(self) -> Dict:
        for required in self._required_fields:
            require_field(instance=self, required_value=required)

        task = self._build_task()
        return task.to_dict()

    def _build_task(self: "ServiceIntegration") -> Task:
        task_fields = [field.name for field in attr.fields(Task)]
        field_name_blacklist = ("Pattern", "Parameters")
        resource_name = self._resource_name.value + self.Pattern.value

        task_kwargs = {}
        parameters_kwargs = {}

        for field in attr.fields(type(self)):
            if field.name in field_name_blacklist or field.name.startswith("_"):
                continue

            value = getattr(self, field.name)
            if value is None:
                continue

            if field.name in task_fields:
                task_kwargs[field.name] = value
            else:
                parameters_kwargs[field.name] = value

        params = Parameters(**parameters_kwargs)
        return Task(Parameters=params, Resource=resource_name, **task_kwargs)


def _supports_patterns(*options: IntegrationPattern) -> Callable[[ServiceIntegration], ServiceIntegration]:
    def _decorate(cls: ServiceIntegration) -> ServiceIntegration:
        cls.Pattern: IntegrationPattern = attr.ib(default=options[0], validator=in_(options))

        return cls

    return _decorate
