"""Amazon SageMaker Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/connect-sagemaker.html
"""
import attr

from rhodes._util import RequiredValue
from rhodes.states.services import IntegrationPattern, ServiceArn, ServiceIntegration, _supports_patterns

__all__ = ("AmazonSageMaker",)

_sagemaker_supports_patterns = _supports_patterns(IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.SYNCHRONOUS)


def _tags(cls: ServiceIntegration) -> ServiceIntegration:
    cls.Tags = attr.ib(default=None)

    return cls


def _endpoint_config_name(cls: ServiceIntegration) -> ServiceIntegration:
    cls.EndpointConfigName = attr.ib(default=None)

    return cls


def _endpoint_name(cls: ServiceIntegration) -> ServiceIntegration:
    cls.EndpointName = attr.ib(default=None)

    return cls


@attr.s(eq=False)
@_sagemaker_supports_patterns
class AmazonSageMaker(ServiceIntegration):
    pass


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

    KmsKeyId = attr.ib(default=None)
    ProductionVariants = attr.ib(default=None)


@attr.s(eq=False)
@_sagemaker_supports_patterns
@_tags
class AmazonSageMakerCreateHyperParameterTuningJob(ServiceIntegration):
    _required_fields = ()
    _resource_name = ServiceArn.SAGEMAKER_CREATE_HYPER_PARAMETER_TUNING_JOB

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateHyperParameterTuningJob.html#API_CreateHyperParameterTuningJob_RequestParameters

    HyperParameterTuningJobConfig = attr.ib(default=None)
    HyperParameterTuningJobName = attr.ib(default=None)
    TrainingJobDefinition = attr.ib(default=None)
    WarmStartConfig = attr.ib(default=None)


@attr.s(eq=False)
@_sagemaker_supports_patterns
@_tags
class AmazonSageMakerCreateLabelingJob(ServiceIntegration):
    _required_fields = ()
    _resource_name = ServiceArn.SAGEMAKER_CREATE_LABELING_JOB

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateLabelingJob.html#API_CreateLabelingJob_RequestParameters

    HumanTaskConfig = attr.ib(default=None)
    InputConfig = attr.ib(default=None)
    LabelAttributeName = attr.ib(default=None)
    LabelCategoryConfigS3Uri = attr.ib(default=None)
    LabelingJobAlgorithmsConfig = attr.ib(default=None)
    LabelingJobName = attr.ib(default=None)
    OutputConfig = attr.ib(default=None)
    RoleArn = attr.ib(default=None)
    StoppingConditions = attr.ib(default=None)


@attr.s(eq=False)
@_sagemaker_supports_patterns
@_tags
class AmazonSageMakerCreateModel(ServiceIntegration):
    _required_fields = ()
    _resource_name = ServiceArn.SAGEMAKER_CREATE_MODEL

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateModel.html#API_CreateModel_RequestParameters

    Containers = attr.ib(default=None)
    EnableNetworkIsolation = attr.ib(default=None)
    ExecutionRoleArn = attr.ib(default=None)
    ModelName = attr.ib(default=None)
    PrimaryContainer = attr.ib(default=None)
    VpcConfig = attr.ib(default=None)


@attr.s(eq=False)
@_sagemaker_supports_patterns
@_tags
class AmazonSageMakerCreateTrainingJob(ServiceIntegration):
    _required_fields = ()
    _resource_name = ServiceArn.SAGEMAKER_CREATE_TRAINING_JOB

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateTrainingJob.html#API_CreateTrainingJob_RequestParameters

    AlgorithmSpecification = attr.ib(default=None)
    HyperParameters = attr.ib(default=None)
    InputDataConfig = attr.ib(default=None)
    OutputDataConfig = attr.ib(default=None)
    ResourceConfig = attr.ib(default=None)
    RoleArn = attr.ib(default=None)
    StoppingCondition = attr.ib(default=None)
    TrainingJobName = attr.ib(default=None)
    VpcConfig = attr.ib(default=None)


@attr.s(eq=False)
@_sagemaker_supports_patterns
@_tags
class AmazonSageMakerCreateTransformJob(ServiceIntegration):
    _required_fields = ()
    _resource_name = ServiceArn.SAGEMAKER_CREATE_TRANSFORM_JOB

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateTransformJob.html#API_CreateTransformJob_RequestParameters

    BatchStrategy = attr.ib(default=None)
    Environment = attr.ib(default=None)
    MaxConcurrentTransforms = attr.ib(default=None)
    MaxPayloadInMB = attr.ib(default=None)
    ModelName = attr.ib(default=None)
    TransformInput = attr.ib(default=None)
    TransformJobName = attr.ib(default=None)
    TransformOutput = attr.ib(default=None)
    TransformResources = attr.ib(default=None)


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
