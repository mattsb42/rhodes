from typing import Any, Optional

from rhodes._types import CATCH, COMMENT, END, HEARTBEAT_SECONDS, NEXT, PATH_INPUT, RETRY, TIMEOUT_SECONDS, TITLE
from rhodes.identifiers import IntegrationPattern
from rhodes.states.services import ServiceIntegration

class AmazonDynamoDb:
    def __init__(self, *, TableName: str): ...
    TableName: str
    def get_item(self, **kwargs) -> AmazonDynamoDbGetItem: ...
    def put_item(self, **kwargs) -> AmazonDynamoDbPutItem: ...
    def delete_item(self, **kwargs) -> AmazonDynamoDbDeleteItem: ...
    def update_item(self, **kwargs) -> AmazonDynamoDbUpdateItem: ...

class AmazonDynamoDbGetItem(ServiceIntegration):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        Next: NEXT = None,
        End: END = None,
        InputPath: PATH_INPUT = None,
        OutputPath: PATH_INPUT = None,
        ResultPath: PATH_INPUT = None,
        Catch: CATCH = None,
        Retry: RETRY = None,
        TimeoutSeconds: TIMEOUT_SECONDS = None,
        HeartbeatSeconds: HEARTBEAT_SECONDS = None,
        TableName: Optional[Any] = None,
        Key: Optional[Any] = None,
        AttributesToGet: Optional[Any] = None,
        ConsistentRead: Optional[Any] = None,
        ExpressionAttributeNames: Optional[Any] = None,
        ProjectionExpression: Optional[Any] = None,
        ReturnConsumedCapacity: Optional[Any] = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
    ): ...
    TableName: Optional[Any]
    Key: Optional[Any]
    AttributesToGet: Optional[Any]
    ConsistentRead: Optional[Any]
    ExpressionAttributeNames: Optional[Any]
    ProjectionExpression: Optional[Any]
    ReturnConsumedCapacity: Optional[Any]
    Pattern: IntegrationPattern

class AmazonDynamoDbPutItem(ServiceIntegration):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        Next: NEXT = None,
        End: END = None,
        InputPath: PATH_INPUT = None,
        OutputPath: PATH_INPUT = None,
        ResultPath: PATH_INPUT = None,
        Catch: CATCH = None,
        Retry: RETRY = None,
        TimeoutSeconds: TIMEOUT_SECONDS = None,
        HeartbeatSeconds: HEARTBEAT_SECONDS = None,
        TableName: Optional[Any] = None,
        Item: Optional[Any] = None,
        ConditionalOperator: Optional[Any] = None,
        ConditionExpression: Optional[Any] = None,
        Expected: Optional[Any] = None,
        ExpressionAttributeNames: Optional[Any] = None,
        ExpressionAttributeValues: Optional[Any] = None,
        ReturnConsumedCapacity: Optional[Any] = None,
        ReturnItemCollectionMetrics: Optional[Any] = None,
        ReturnValues: Optional[Any] = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
    ): ...
    TableName: Optional[Any]
    Item: Optional[Any]
    ConditionalOperator: Optional[Any]
    ConditionExpression: Optional[Any]
    Expected: Optional[Any]
    ExpressionAttributeNames: Optional[Any]
    ExpressionAttributeValues: Optional[Any]
    ReturnConsumedCapacity: Optional[Any]
    ReturnItemCollectionMetrics: Optional[Any]
    ReturnValues: Optional[Any]
    Pattern: IntegrationPattern

class AmazonDynamoDbDeleteItem(ServiceIntegration):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        Next: NEXT = None,
        End: END = None,
        InputPath: PATH_INPUT = None,
        OutputPath: PATH_INPUT = None,
        ResultPath: PATH_INPUT = None,
        Catch: CATCH = None,
        Retry: RETRY = None,
        TimeoutSeconds: TIMEOUT_SECONDS = None,
        HeartbeatSeconds: HEARTBEAT_SECONDS = None,
        TableName: Optional[Any] = None,
        Key: Optional[Any] = None,
        ConditionalOperator: Optional[Any] = None,
        ConditionExpression: Optional[Any] = None,
        Expected: Optional[Any] = None,
        ExpressionAttributeNames: Optional[Any] = None,
        ExpressionAttributeValues: Optional[Any] = None,
        ReturnConsumedCapacity: Optional[Any] = None,
        ReturnItemCollectionMetrics: Optional[Any] = None,
        ReturnValues: Optional[Any] = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
    ): ...
    TableName: Optional[Any]
    Key: Optional[Any]
    ConditionalOperator: Optional[Any]
    ConditionExpression: Optional[Any]
    Expected: Optional[Any]
    ExpressionAttributeNames: Optional[Any]
    ExpressionAttributeValues: Optional[Any]
    ReturnConsumedCapacity: Optional[Any]
    ReturnItemCollectionMetrics: Optional[Any]
    ReturnValues: Optional[Any]
    Pattern: IntegrationPattern

class AmazonDynamoDbUpdateItem(ServiceIntegration):
    def __init__(
        self,
        title: TITLE,
        *,
        Comment: COMMENT = None,
        Next: NEXT = None,
        End: END = None,
        InputPath: PATH_INPUT = None,
        OutputPath: PATH_INPUT = None,
        ResultPath: PATH_INPUT = None,
        Catch: CATCH = None,
        Retry: RETRY = None,
        TimeoutSeconds: TIMEOUT_SECONDS = None,
        HeartbeatSeconds: HEARTBEAT_SECONDS = None,
        TableName: Optional[Any] = None,
        Key: Optional[Any] = None,
        ConditionalOperator: Optional[Any] = None,
        ConditionExpression: Optional[Any] = None,
        Expected: Optional[Any] = None,
        ExpressionAttributeNames: Optional[Any] = None,
        ExpressionAttributeValues: Optional[Any] = None,
        ReturnConsumedCapacity: Optional[Any] = None,
        ReturnItemCollectionMetrics: Optional[Any] = None,
        ReturnValues: Optional[Any] = None,
        AttributeUpdates: Optional[Any] = None,
        UpdateExpression: Optional[Any] = None,
        Pattern: IntegrationPattern = IntegrationPattern.REQUEST_RESPONSE,
    ): ...
    TableName: Optional[Any]
    Key: Optional[Any]
    ConditionalOperator: Optional[Any]
    ConditionExpression: Optional[Any]
    Expected: Optional[Any]
    ExpressionAttributeNames: Optional[Any]
    ExpressionAttributeValues: Optional[Any]
    ReturnConsumedCapacity: Optional[Any]
    ReturnItemCollectionMetrics: Optional[Any]
    ReturnValues: Optional[Any]
    AttributeUpdates: Optional[Any]
    UpdateExpression: Optional[Any]
    Pattern: IntegrationPattern
