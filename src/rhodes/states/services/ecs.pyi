from typing import Any, Optional

from rhodes._types import CATCH, COMMENT, END, HEARTBEAT_SECONDS, NEXT, PATH_INPUT, RETRY, TIMEOUT_SECONDS, TITLE
from rhodes.identifiers import IntegrationPattern
from rhodes.states.services import ServiceIntegration
from rhodes.structures import JsonPath, Parameters

class AmazonEcs(ServiceIntegration):
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
        Cluster: Optional[Any] = None,
        Group: Optional[Any] = None,
        LaunchType: Optional[Any] = None,
        NetworkConfiguration: Optional[Any] = None,
        Overrides: Optional[Any] = None,
        PlacementConstraints: Optional[Any] = None,
        PlacementStrategy: Optional[Any] = None,
        PlatformVersion: Optional[Any] = None,
        TaskDefinition: Optional[Any] = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
    ): ...
    Pattern: IntegrationPattern
    Cluster: Optional[Any]
    Group: Optional[Any]
    LaunchType: Optional[Any]
    NetworkConfiguration: Optional[Any]
    Overrides: Optional[Any]
    PlacementConstraints: Optional[Any]
    PlacementStrategy: Optional[Any]
    PlatformVersion: Optional[Any]
    TaskDefinition: Optional[Any]
