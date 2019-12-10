"""Amazon SageMaker Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/connect-sagemaker.html
"""
import attr

from rhodes._util import RHODES_ATTRIB, RequiredValue
from rhodes.identifiers import IntegrationPattern, ServiceArn
from rhodes.states.services import ServiceIntegration
from rhodes.states.services.util import supports_patterns

__all__ = (
    "AmazonSageMakerCreateEndpoint",
    "AmazonSageMakerCreateEndpointConfig",
    "AmazonSageMakerCreateHyperParameterTuningJob",
    "AmazonSageMakerCreateLabelingJob",
    "AmazonSageMakerCreateModel",
    "AmazonSageMakerCreateTrainingJob",
    "AmazonSageMakerCreateTransformJob",
    "AmazonSageMakerUpdateEndpoint",
)

_sagemaker_supports_patterns = supports_patterns(IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.SYNCHRONOUS)


def _tags(cls: ServiceIntegration) -> ServiceIntegration:
    cls.Tags = RHODES_ATTRIB()

    return cls


def _endpoint_config_name(cls: ServiceIntegration) -> ServiceIntegration:
    cls.EndpointConfigName = RHODES_ATTRIB()

    return cls


def _endpoint_name(cls: ServiceIntegration) -> ServiceIntegration:
    cls.EndpointName = RHODES_ATTRIB()

    return cls


# TODO: Create an AamzonSageMaker single entry point helper like AmazonDynamoDb


@attr.s(eq=False)
@_sagemaker_supports_patterns
@_tags
@_endpoint_name
@_endpoint_config_name
class AmazonSageMakerCreateEndpoint(ServiceIntegration):
    _required_fields = ()
    _resource_name = ServiceArn.SAGEMAKER_CREATE_ENDPOINT

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateEndpoint.html#API_CreateEndpoint_RequestParameters


@attr.s(eq=False)
@_sagemaker_supports_patterns
@_tags
@_endpoint_config_name
class AmazonSageMakerCreateEndpointConfig(ServiceIntegration):
    _required_fields = ()
    _resource_name = ServiceArn.SAGEMAKER_CREATE_ENDPOINT_CONFIG

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateEndpointConfig.html#API_CreateEndpointConfig_RequestParameters

    KmsKeyId = RHODES_ATTRIB()
    ProductionVariants = RHODES_ATTRIB()


@attr.s(eq=False)
@_sagemaker_supports_patterns
@_tags
class AmazonSageMakerCreateHyperParameterTuningJob(ServiceIntegration):
    _required_fields = ()
    _resource_name = ServiceArn.SAGEMAKER_CREATE_HYPER_PARAMETER_TUNING_JOB

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateHyperParameterTuningJob.html#API_CreateHyperParameterTuningJob_RequestParameters

    HyperParameterTuningJobConfig = RHODES_ATTRIB()
    HyperParameterTuningJobName = RHODES_ATTRIB()
    TrainingJobDefinition = RHODES_ATTRIB()
    WarmStartConfig = RHODES_ATTRIB()


@attr.s(eq=False)
@_sagemaker_supports_patterns
@_tags
class AmazonSageMakerCreateLabelingJob(ServiceIntegration):
    _required_fields = ()
    _resource_name = ServiceArn.SAGEMAKER_CREATE_LABELING_JOB

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateLabelingJob.html#API_CreateLabelingJob_RequestParameters

    HumanTaskConfig = RHODES_ATTRIB()
    InputConfig = RHODES_ATTRIB()
    LabelAttributeName = RHODES_ATTRIB()
    LabelCategoryConfigS3Uri = RHODES_ATTRIB()
    LabelingJobAlgorithmsConfig = RHODES_ATTRIB()
    LabelingJobName = RHODES_ATTRIB()
    OutputConfig = RHODES_ATTRIB()
    RoleArn = RHODES_ATTRIB()
    StoppingConditions = RHODES_ATTRIB()


@attr.s(eq=False)
@_sagemaker_supports_patterns
@_tags
class AmazonSageMakerCreateModel(ServiceIntegration):
    _required_fields = ()
    _resource_name = ServiceArn.SAGEMAKER_CREATE_MODEL

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateModel.html#API_CreateModel_RequestParameters

    Containers = RHODES_ATTRIB()
    EnableNetworkIsolation = RHODES_ATTRIB()
    ExecutionRoleArn = RHODES_ATTRIB()
    ModelName = RHODES_ATTRIB()
    PrimaryContainer = RHODES_ATTRIB()
    VpcConfig = RHODES_ATTRIB()


@attr.s(eq=False)
@_sagemaker_supports_patterns
@_tags
class AmazonSageMakerCreateTrainingJob(ServiceIntegration):
    _required_fields = ()
    _resource_name = ServiceArn.SAGEMAKER_CREATE_TRAINING_JOB

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateTrainingJob.html#API_CreateTrainingJob_RequestParameters

    AlgorithmSpecification = RHODES_ATTRIB()
    HyperParameters = RHODES_ATTRIB()
    InputDataConfig = RHODES_ATTRIB()
    OutputDataConfig = RHODES_ATTRIB()
    ResourceConfig = RHODES_ATTRIB()
    RoleArn = RHODES_ATTRIB()
    StoppingCondition = RHODES_ATTRIB()
    TrainingJobName = RHODES_ATTRIB()
    VpcConfig = RHODES_ATTRIB()


@attr.s(eq=False)
@_sagemaker_supports_patterns
@_tags
class AmazonSageMakerCreateTransformJob(ServiceIntegration):
    _required_fields = ()
    _resource_name = ServiceArn.SAGEMAKER_CREATE_TRANSFORM_JOB

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateTransformJob.html#API_CreateTransformJob_RequestParameters

    BatchStrategy = RHODES_ATTRIB()
    Environment = RHODES_ATTRIB()
    MaxConcurrentTransforms = RHODES_ATTRIB()
    MaxPayloadInMB = RHODES_ATTRIB()
    ModelName = RHODES_ATTRIB()
    TransformInput = RHODES_ATTRIB()
    TransformJobName = RHODES_ATTRIB()
    TransformOutput = RHODES_ATTRIB()
    TransformResources = RHODES_ATTRIB()


@attr.s(eq=False)
@_sagemaker_supports_patterns
@_tags
@_endpoint_name
@_endpoint_config_name
class AmazonSageMakerUpdateEndpoint(ServiceIntegration):
    _required_fields = ()
    _resource_name = ServiceArn.SAGEMAKER_UPDATE_ENDPOINT

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sagemaker/latest/dg/API_UpdateEndpoint.html#API_UpdateEndpoint_RequestParameters
