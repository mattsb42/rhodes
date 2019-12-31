from typing import Any, Optional

from rhodes._types import (
    CATCH,
    COMMENT,
    END,
    HEARTBEAT_SECONDS,
    INPUT_PATH,
    NEXT,
    OUTPUT_PATH,
    PATH_INPUT,
    RESULT_PATH,
    RETRY,
    TIMEOUT_SECONDS,
    TITLE,
    StateMirror,
)
from rhodes.identifiers import IntegrationPattern
from rhodes.states import State
from rhodes.structures import JsonPath, Parameters

ENDPOINT_CONFIG_NAME = Optional[Any]
ENDPOINT_NAME = Optional[Any]
TAGS = Optional[Any]

class AmazonSageMakerCreateEndpoint(State):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        Next: NEXT = None,
        End: END = None,
        InputPath: PATH_INPUT = JsonPath("$"),
        OutputPath: PATH_INPUT = JsonPath("$"),
        ResultPath: PATH_INPUT = JsonPath("$"),
        Catch: CATCH = None,
        Retry: RETRY = None,
        TimeoutSeconds: TIMEOUT_SECONDS = None,
        HeartbeatSeconds: HEARTBEAT_SECONDS = None,
        EndpointConfigName: ENDPOINT_CONFIG_NAME = None,
        EndpointName: ENDPOINT_NAME = None,
        Tags: TAGS = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
    ): ...
    Next: NEXT
    End: END
    InputPath: INPUT_PATH
    OutputPath: OUTPUT_PATH
    ResultPath: RESULT_PATH
    Catch: CATCH
    Retry: RETRY
    TimeoutSeconds: TIMEOUT_SECONDS
    HeartbeatSeconds: HEARTBEAT_SECONDS
    def then(self, next_state: StateMirror) -> StateMirror: ...
    def end(self) -> State: ...
    EndpointConfigName: ENDPOINT_CONFIG_NAME
    EndpointName: ENDPOINT_NAME
    Tags: TAGS
    Pattern: IntegrationPattern

class AmazonSageMakerCreateEndpointConfig(State):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        Next: NEXT = None,
        End: END = None,
        InputPath: PATH_INPUT = JsonPath("$"),
        OutputPath: PATH_INPUT = JsonPath("$"),
        ResultPath: PATH_INPUT = JsonPath("$"),
        Catch: CATCH = None,
        Retry: RETRY = None,
        TimeoutSeconds: TIMEOUT_SECONDS = None,
        HeartbeatSeconds: HEARTBEAT_SECONDS = None,
        EndpointConfigName: ENDPOINT_CONFIG_NAME = None,
        Tags: TAGS = None,
        KmsKeyId: Optional[Any] = None,
        ProductionVariants: Optional[Any] = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
    ): ...
    Next: NEXT
    End: END
    InputPath: INPUT_PATH
    OutputPath: OUTPUT_PATH
    ResultPath: RESULT_PATH
    Catch: CATCH
    Retry: RETRY
    TimeoutSeconds: TIMEOUT_SECONDS
    HeartbeatSeconds: HEARTBEAT_SECONDS
    def then(self, next_state: StateMirror) -> StateMirror: ...
    def end(self) -> State: ...
    EndpointConfigName: ENDPOINT_CONFIG_NAME
    Tags: TAGS
    KmsKeyId: Optional[Any]
    ProductionVariants: Optional[Any]
    Pattern: IntegrationPattern

class AmazonSageMakerCreateHyperParameterTuningJob(State):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        Next: NEXT = None,
        End: END = None,
        InputPath: PATH_INPUT = JsonPath("$"),
        OutputPath: PATH_INPUT = JsonPath("$"),
        ResultPath: PATH_INPUT = JsonPath("$"),
        Catch: CATCH = None,
        Retry: RETRY = None,
        TimeoutSeconds: TIMEOUT_SECONDS = None,
        HeartbeatSeconds: HEARTBEAT_SECONDS = None,
        Tags: TAGS = None,
        HyperParameterTuningJobConfig: Optional[Any] = None,
        HyperParameterTuningJobName: Optional[Any] = None,
        TrainingJobDefinition: Optional[Any] = None,
        WarmStartConfig: Optional[Any] = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
    ): ...
    Next: NEXT
    End: END
    InputPath: INPUT_PATH
    OutputPath: OUTPUT_PATH
    ResultPath: RESULT_PATH
    Catch: CATCH
    Retry: RETRY
    TimeoutSeconds: TIMEOUT_SECONDS
    HeartbeatSeconds: HEARTBEAT_SECONDS
    def then(self, next_state: StateMirror) -> StateMirror: ...
    def end(self) -> State: ...
    Tags: TAGS
    HyperParameterTuningJobConfig: Optional[Any]
    HyperParameterTuningJobName: Optional[Any]
    TrainingJobDefinition: Optional[Any]
    WarmStartConfig: Optional[Any]
    Pattern: IntegrationPattern

class AmazonSageMakerCreateLabelingJob(State):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        Next: NEXT = None,
        End: END = None,
        InputPath: PATH_INPUT = JsonPath("$"),
        OutputPath: PATH_INPUT = JsonPath("$"),
        ResultPath: PATH_INPUT = JsonPath("$"),
        Catch: CATCH = None,
        Retry: RETRY = None,
        TimeoutSeconds: TIMEOUT_SECONDS = None,
        HeartbeatSeconds: HEARTBEAT_SECONDS = None,
        Tags: TAGS = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
        HumanTaskConfig: Optional[Any] = None,
        InputConfig: Optional[Any] = None,
        LabelAttributeName: Optional[Any] = None,
        LabelCategoryConfigS3Uri: Optional[Any] = None,
        LabelingJobAlgorithmsConfig: Optional[Any] = None,
        LabelingJobName: Optional[Any] = None,
        OutputConfig: Optional[Any] = None,
        RoleArn: Optional[Any] = None,
        StoppingConditions: Optional[Any] = None,
    ): ...
    Next: NEXT
    End: END
    InputPath: INPUT_PATH
    OutputPath: OUTPUT_PATH
    ResultPath: RESULT_PATH
    Catch: CATCH
    Retry: RETRY
    TimeoutSeconds: TIMEOUT_SECONDS
    HeartbeatSeconds: HEARTBEAT_SECONDS
    def then(self, next_state: StateMirror) -> StateMirror: ...
    def end(self) -> State: ...
    Tags: TAGS
    Pattern: IntegrationPattern
    HumanTaskConfig: Optional[Any]
    InputConfig: Optional[Any]
    LabelAttributeName: Optional[Any]
    LabelCategoryConfigS3Uri: Optional[Any]
    LabelingJobAlgorithmsConfig: Optional[Any]
    LabelingJobName: Optional[Any]
    OutputConfig: Optional[Any]
    RoleArn: Optional[Any]
    StoppingConditions: Optional[Any]

class AmazonSageMakerCreateModel(State):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        Next: NEXT = None,
        End: END = None,
        InputPath: PATH_INPUT = JsonPath("$"),
        OutputPath: PATH_INPUT = JsonPath("$"),
        ResultPath: PATH_INPUT = JsonPath("$"),
        Catch: CATCH = None,
        Retry: RETRY = None,
        TimeoutSeconds: TIMEOUT_SECONDS = None,
        HeartbeatSeconds: HEARTBEAT_SECONDS = None,
        Tags: TAGS = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
        Containers: Optional[Any] = None,
        EnableNetworkIsolation: Optional[Any] = None,
        ExecutionRoleArn: Optional[Any] = None,
        ModelName: Optional[Any] = None,
        PrimaryContainer: Optional[Any] = None,
        VpcConfig: Optional[Any] = None,
    ): ...
    Next: NEXT
    End: END
    InputPath: INPUT_PATH
    OutputPath: OUTPUT_PATH
    ResultPath: RESULT_PATH
    Catch: CATCH
    Retry: RETRY
    TimeoutSeconds: TIMEOUT_SECONDS
    HeartbeatSeconds: HEARTBEAT_SECONDS
    def then(self, next_state: StateMirror) -> StateMirror: ...
    def end(self) -> State: ...
    Tags: TAGS
    Pattern: IntegrationPattern
    Containers: Optional[Any]
    EnableNetworkIsolation: Optional[Any]
    ExecutionRoleArn: Optional[Any]
    ModelName: Optional[Any]
    PrimaryContainer: Optional[Any]
    VpcConfig: Optional[Any]

class AmazonSageMakerCreateTrainingJob(State):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        Next: NEXT = None,
        End: END = None,
        InputPath: PATH_INPUT = JsonPath("$"),
        OutputPath: PATH_INPUT = JsonPath("$"),
        ResultPath: PATH_INPUT = JsonPath("$"),
        Catch: CATCH = None,
        Retry: RETRY = None,
        TimeoutSeconds: TIMEOUT_SECONDS = None,
        HeartbeatSeconds: HEARTBEAT_SECONDS = None,
        Tags: TAGS = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
        AlgorithmSpecification: Optional[Any] = None,
        HyperParameters: Optional[Any] = None,
        InputDataConfig: Optional[Any] = None,
        OutputDataConfig: Optional[Any] = None,
        ResourceConfig: Optional[Any] = None,
        RoleArn: Optional[Any] = None,
        StoppingCondition: Optional[Any] = None,
        TrainingJobName: Optional[Any] = None,
        VpcConfig: Optional[Any] = None,
    ): ...
    Next: NEXT
    End: END
    InputPath: INPUT_PATH
    OutputPath: OUTPUT_PATH
    ResultPath: RESULT_PATH
    Catch: CATCH
    Retry: RETRY
    TimeoutSeconds: TIMEOUT_SECONDS
    HeartbeatSeconds: HEARTBEAT_SECONDS
    def then(self, next_state: StateMirror) -> StateMirror: ...
    def end(self) -> State: ...
    Tags: TAGS
    Pattern: IntegrationPattern
    AlgorithmSpecification: Optional[Any]
    HyperParameters: Optional[Any]
    InputDataConfig: Optional[Any]
    OutputDataConfig: Optional[Any]
    ResourceConfig: Optional[Any]
    RoleArn: Optional[Any]
    StoppingCondition: Optional[Any]
    TrainingJobName: Optional[Any]
    VpcConfig: Optional[Any]

class AmazonSageMakerCreateTransformJob(State):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        Next: NEXT = None,
        End: END = None,
        InputPath: PATH_INPUT = JsonPath("$"),
        OutputPath: PATH_INPUT = JsonPath("$"),
        ResultPath: PATH_INPUT = JsonPath("$"),
        Catch: CATCH = None,
        Retry: RETRY = None,
        TimeoutSeconds: TIMEOUT_SECONDS = None,
        HeartbeatSeconds: HEARTBEAT_SECONDS = None,
        Tags: TAGS = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
        BatchStrategy: Optional[Any] = None,
        Environment: Optional[Any] = None,
        MaxConcurrentTransforms: Optional[Any] = None,
        MaxPayloadInMB: Optional[Any] = None,
        ModelName: Optional[Any] = None,
        TransformInput: Optional[Any] = None,
        TransformJobName: Optional[Any] = None,
        TransformOutput: Optional[Any] = None,
        TransformResources: Optional[Any] = None,
    ): ...
    Next: NEXT
    End: END
    InputPath: INPUT_PATH
    OutputPath: OUTPUT_PATH
    ResultPath: RESULT_PATH
    Catch: CATCH
    Retry: RETRY
    TimeoutSeconds: TIMEOUT_SECONDS
    HeartbeatSeconds: HEARTBEAT_SECONDS
    def then(self, next_state: StateMirror) -> StateMirror: ...
    def end(self) -> State: ...
    Tags: TAGS
    Pattern: IntegrationPattern
    BatchStrategy: Optional[Any]
    Environment: Optional[Any]
    MaxConcurrentTransforms: Optional[Any]
    MaxPayloadInMB: Optional[Any]
    ModelName: Optional[Any]
    TransformInput: Optional[Any]
    TransformJobName: Optional[Any]
    TransformOutput: Optional[Any]
    TransformResources: Optional[Any]

class AmazonSageMakerUpdateEndpoint(State):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        Next: NEXT = None,
        End: END = None,
        InputPath: PATH_INPUT = JsonPath("$"),
        OutputPath: PATH_INPUT = JsonPath("$"),
        ResultPath: PATH_INPUT = JsonPath("$"),
        Catch: CATCH = None,
        Retry: RETRY = None,
        TimeoutSeconds: TIMEOUT_SECONDS = None,
        HeartbeatSeconds: HEARTBEAT_SECONDS = None,
        EndpointConfigName: ENDPOINT_CONFIG_NAME = None,
        EndpointName: ENDPOINT_NAME = None,
        Tags: TAGS = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
    ): ...
    Next: NEXT
    End: END
    InputPath: INPUT_PATH
    OutputPath: OUTPUT_PATH
    ResultPath: RESULT_PATH
    Catch: CATCH
    Retry: RETRY
    TimeoutSeconds: TIMEOUT_SECONDS
    HeartbeatSeconds: HEARTBEAT_SECONDS
    def then(self, next_state: StateMirror) -> StateMirror: ...
    def end(self) -> State: ...
    EndpointConfigName: ENDPOINT_CONFIG_NAME
    EndpointName: ENDPOINT_NAME
    Tags: TAGS
    Pattern: IntegrationPattern
