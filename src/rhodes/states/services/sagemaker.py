"""
`Amazon SageMaker <https://docs.aws.amazon.com/step-functions/latest/dg/connect-sagemaker.html>`_ Task states.
"""
import attr

from rhodes._types import StateMirror
from rhodes._util import RHODES_ATTRIB, RequiredValue, docstring_with_param
from rhodes.identifiers import IntegrationPattern, ServiceArn
from rhodes.states import State
from rhodes.states.services._util import service_integration

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

_sagemaker_service_integration = service_integration(
    IntegrationPattern.REQUEST_RESPONSE, IntegrationPattern.SYNCHRONOUS
)


def _tags(cls: StateMirror) -> StateMirror:
    cls.Tags = RHODES_ATTRIB()
    cls.__doc__ = docstring_with_param(
        cls,
        "Tags",
        description=(
            "An array of key-value pairs. "
            "For more information, see Using Cost Allocation Tagsin the AWS Billing and Cost Management User Guide."
        ),
    )

    return cls


def _endpoint_config_name(cls: StateMirror) -> StateMirror:
    cls.EndpointConfigName = RHODES_ATTRIB()
    cls.__doc__ = docstring_with_param(cls, "EndpointConfigName", description="The name of an endpoint configuration.")

    return cls


def _endpoint_name(cls: StateMirror) -> StateMirror:
    cls.EndpointName = RHODES_ATTRIB()
    cls.__doc__ = docstring_with_param(cls, "EndpointName", description="The name of the endpoint.")

    return cls


# TODO: Create an AamzonSageMaker single entry point helper like AmazonDynamoDb


@attr.s(eq=False)
@_tags
@_endpoint_name
@_endpoint_config_name
@_sagemaker_service_integration
class AmazonSageMakerCreateEndpoint(State):
    """"""

    _required_fields = ()
    _resource_name = ServiceArn.SAGEMAKER_CREATE_ENDPOINT

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateEndpoint.html#API_CreateEndpoint_RequestParameters


@attr.s(eq=False)
@_tags
@_endpoint_config_name
@_sagemaker_service_integration
class AmazonSageMakerCreateEndpointConfig(State):
    """
    :param KmsKeyId: The Amazon Resource Name (ARN) of a AWS Key Management Service key
       that Amazon SageMaker uses to encrypt data on the storage volume
       attached to the ML compute instance that hosts the endpoint.
    :param ProductionVariants: An list of ProductionVariant objects,
       one for each model that you want to host at this endpoint.
    """

    _required_fields = ()
    _resource_name = ServiceArn.SAGEMAKER_CREATE_ENDPOINT_CONFIG

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateEndpointConfig.html#API_CreateEndpointConfig_RequestParameters

    KmsKeyId = RHODES_ATTRIB()
    ProductionVariants = RHODES_ATTRIB()


@attr.s(eq=False)
@_tags
@_sagemaker_service_integration
class AmazonSageMakerCreateHyperParameterTuningJob(State):
    """
    :param HyperParameterTuningJobConfig: The HyperParameterTuningJobConfig object that describes the tuning job,
       including the search strategy, the objective metric used to evaluate training jobs,
       ranges of parameters to search, and resource limits for the tuning job.
    :param HyperParameterTuningJobName: The name of the tuning job.
       This name is the prefix for the names of all training jobs that this tuning job launches.
       The name must be unique within the same AWS account and AWS Region. The name must have { } to { } characters.
       Valid characters are a-z, A-Z, 0-9, and : + = @ _ % - (hyphen). The name is not case sensitive.
    :param TrainingJobDefinition:
       The HyperParameterTrainingJobDefinition object that describes the training jobs that this tuning job launches,
       including static hyperparameters, input data configuration, output data configuration, resource configuration,
       and stopping condition.
    :param WarmStartConfig:
       Specifies the configuration for starting the hyperparameter tuning job
       using one or more previous tuning jobs as a starting point.
       The results of previous tuning jobs are used to inform which combinations of hyperparameters to search over
       in the new tuning job.
    """

    _required_fields = ()
    _resource_name = ServiceArn.SAGEMAKER_CREATE_HYPER_PARAMETER_TUNING_JOB

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateHyperParameterTuningJob.html#API_CreateHyperParameterTuningJob_RequestParameters

    HyperParameterTuningJobConfig = RHODES_ATTRIB()
    HyperParameterTuningJobName = RHODES_ATTRIB()
    TrainingJobDefinition = RHODES_ATTRIB()
    WarmStartConfig = RHODES_ATTRIB()


@attr.s(eq=False)
@_tags
@_sagemaker_service_integration
class AmazonSageMakerCreateLabelingJob(State):
    """
    :param HumanTaskConfig: Configures the labeling task and how it is presented to workers;
       including, but not limited to price, keywords, and batch size (task count).
    :param InputConfig: Input data for the labeling job, such as the Amazon S3 location of the data objects
       and the location of the manifest file that describes the data objects.
    :param LabelAttributeName: The attribute name to use for the label in the output manifest file.
    :param LabelCategoryConfigS3Uri: The S3 URL of the file that defines the categories used to label the data objects.
    :param LabelingJobAlgorithmsConfig: Configures the information required to perform automated data labeling.
    :param LabelingJobName: The name of the labeling job.
       This name is used to identify the job in a list of labeling jobs.
    :param OutputConfig: The location of the output data and the AWS Key Management Service key ID
       for the key used to encrypt the output data, if any.
    :param RoleArn: The Amazon Resource Number (ARN) that Amazon SageMaker assumes
       to perform tasks on your behalf during data labeling.
       You must grant this role the necessary permissions
       so that Amazon SageMaker can successfully complete data labeling.
    :param StoppingConditions: A set of conditions for stopping the labeling job.
       If any of the conditions are met, the job is automatically stopped.
       You can use these conditions to control the cost of data labeling.
    """

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
@_tags
@_sagemaker_service_integration
class AmazonSageMakerCreateModel(State):
    """
    :param Containers: Specifies the containers in the inference pipeline.
    :param EnableNetworkIsolation: Isolates the model container.
       No inbound or outbound network calls can be made to or from the model container.
    :param ExecutionRoleArn: The Amazon Resource Name (ARN) of the IAM role that Amazon SageMaker can assume
       to access model artifacts and docker image for deployment on ML compute instances or for batch transform jobs.
       Deploying on ML compute instances is part of model hosting. For more information, see Amazon SageMaker Roles.
    :param ModelName: The name of the new model.
    :param PrimaryContainer: The location of the primary docker image containing inference code, associated artifacts,
       and custom environment map that the inference code uses when the model is deployed for predictions.
    :param VpcConfig: A VpcConfig object that specifies the VPC that you want your model to connect to.
    """

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
@_tags
@_sagemaker_service_integration
class AmazonSageMakerCreateTrainingJob(State):
    """
    :param AlgorithmSpecification: The registry path of the Docker image that contains the training algorithm
       and algorithm-specific metadata, including the input mode.
    :param HyperParameters: Algorithm-specific parameters that influence the quality of the model.
       You set hyperparameters before you start the learning process.
    :param InputDataConfig: An array of Channel objects. Each channel is a named input source.
       InputDataConfig describes the input data and its location.
    :param OutputDataConfig: Specifies the path to the S3 location where you want to store model artifacts.
       Amazon SageMaker creates subfolders for the artifacts.
    :param ResourceConfig:
       The resources, including the ML compute instances and ML storage volumes, to use for model training.
    :param RoleArn:
       The Amazon Resource Name (ARN) of an IAM role that Amazon SageMaker can assume to perform tasks on your behalf.
    :param StoppingCondition: Specifies a limit to how long a model training job can run.
       When the job reaches the time limit, Amazon SageMaker ends the training job.
       Use this API to cap model training costs.
    :param TrainingJobName: The name of the training job.
       The name must be unique within an AWS Region in an AWS account.
    :param VpcConfig: A VpcConfig object that specifies the VPC that you want your training job to connect to.
    """

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
@_tags
@_sagemaker_service_integration
class AmazonSageMakerCreateTransformJob(State):
    """
    :param BatchStrategy: Specifies the number of records to include in a mini-batch for an HTTP inference request.
       A record is a single unit of input data that inference can be made on.
       For example, a single line in a CSV file is a record.
    :param Environment: The environment variables to set in the Docker container.
    :param MaxConcurrentTransforms:
       The maximum number of parallel requests that can be sent to each instance in a transform job.
    :param MaxPayloadInMB: The maximum allowed size of the payload, in MB.
    :param ModelName: The name of the model that you want to use for the transform job.
       ModelName must be the name of an existing Amazon SageMaker model within an AWS Region in an AWS account.
    :param TransformInput: Describes the input source and the way the transform job consumes it.
    :param TransformJobName: The name of the transform job.
       The name must be unique within an AWS Region in an AWS account.
    :param TransformOutput: Describes the results of the transform job.
    :param TransformResources:
       Describes the resources, including ML instance types and ML instance count, to use for the transform job.
    """

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
@_tags
@_endpoint_name
@_endpoint_config_name
@_sagemaker_service_integration
class AmazonSageMakerUpdateEndpoint(State):
    """"""

    _required_fields = ()
    _resource_name = ServiceArn.SAGEMAKER_UPDATE_ENDPOINT

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/sagemaker/latest/dg/API_UpdateEndpoint.html#API_UpdateEndpoint_RequestParameters
