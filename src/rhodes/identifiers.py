"""Static identifiers used within Rhodes."""
from enum import Enum

__all__ = ("ServiceArn", "IntegrationPattern")

_DDB_BASE_ARN = "arn:aws:states:::dynamodb"
_SAGEMAKER_BASE_ARN = "arn:aws:states:::sagemaker"


class ServiceArn(Enum):
    """Step Functions `service integrations`_ ARNs.

    Used as ``Resource`` value when creating a :class:`Task`
    that uses one of these `service integrations`_.

    .. _service integrations: https://docs.aws.amazon.com/step-functions/latest/dg/concepts-service-integrations.html
    """

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
    """Service integration pattern types.

    Used either when building a `service integration`_ :class:`Task` manually
    or when configuring a :class:`ServiceIntegration` helper class.

    .. _service integration: https://docs.aws.amazon.com/step-functions/latest/dg/concepts-service-integrations.html
    """

    REQUEST_RESPONSE = ""
    SYNCHRONOUS = ".sync"
    WAIT_FOR_CALLBACK = ".waitForTaskToken"
