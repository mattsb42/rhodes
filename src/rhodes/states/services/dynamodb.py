"""Amazon DynamoDB Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/connect-ddb.html
"""
import attr
from attr.validators import instance_of

from rhodes._util import RequiredValue
from rhodes.states.services import IntegrationPattern, ServiceArn, ServiceIntegration, _supports_patterns

__all__ = (
    "AmazonDynamoDb",
    "AmazonDynamoDbGetItem",
    "AmazonDynamoDbPutItem",
    "AmazonDynamoDbDeleteItem",
    "AmazonDynamoDbUpdateItem",
)

_ddb_supports_patterns = _supports_patterns(IntegrationPattern.REQUEST_RESPONSE)


class AmazonDynamoDb:
    TableName = attr.ib(validator=instance_of(str))

    def get_item(self, **kwargs):
        return AmazonDynamoDbGetItem(TableName=self.TableName, **kwargs)

    def put_item(self, **kwargs):
        return AmazonDynamoDbPutItem(TableName=self.TableName, **kwargs)

    def delete_item(self, **kwargs):
        return AmazonDynamoDbDeleteItem(TableName=self.TableName, **kwargs)

    def update_item(self, **kwargs):
        return AmazonDynamoDbUpdateItem(TableName=self.TableName, **kwargs)


def _ddb_table_name(cls: ServiceIntegration) -> ServiceIntegration:
    cls.TableName = attr.ib(default=None)

    return cls


def _ddb_key(cls: ServiceIntegration) -> ServiceIntegration:
    cls.Key = attr.ib(default=None)

    return cls


def _ddb_write_attributes(cls: ServiceIntegration) -> ServiceIntegration:
    cls.ConditionalOperator = attr.ib(default=None)
    cls.ConditionExpression = attr.ib(default=None)
    cls.Expected = attr.ib(default=None)
    cls.ExpressionAttributeNames = attr.ib(default=None)
    cls.ExpressionAttributeValues = attr.ib(default=None)
    cls.ReturnConsumedCapacity = attr.ib(default=None)
    cls.ReturnItemCollectionMetrics = attr.ib(default=None)
    cls.ReturnValues = attr.ib(default=None)

    return cls


@attr.s(eq=False)
@_ddb_key
@_ddb_table_name
@_ddb_supports_patterns
class AmazonDynamoDbGetItem(IntegrationPattern):
    _required_fields = (
        RequiredValue("Key", "Amazon DynamoDB GetItem Task requires a key value"),
        RequiredValue("TableName", "Amazon DynamoDB GetItem Task requires a table value"),
    )
    _resource_name = ServiceArn.DYNAMODB_GET_ITEM

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html#DDB-GetItem-request-Key

    AttributesToGet = attr.ib(default=None)
    ConsistentRead = attr.ib(default=None)
    ExpressionAttributeNames = attr.ib(default=None)
    ProjectionExpression = attr.ib(default=None)
    ReturnConsumedCapacity = attr.ib(default=None)


@attr.s(eq=False)
@_ddb_write_attributes
@_ddb_table_name
@_ddb_supports_patterns
class AmazonDynamoDbPutItem(IntegrationPattern):
    _required_fields = (
        RequiredValue("Item", "Amazon DynamoDB PutItem Task requires an item value"),
        RequiredValue("TableName", "Amazon DynamoDB PutItem Task requires a table value"),
    )
    _resource_name = ServiceArn.DYNAMODB_PUT_ITEM

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html#DDB-PutItem-request-Item

    Item = attr.ib(default=None)


@attr.s(eq=False)
@_ddb_write_attributes
@_ddb_key
@_ddb_table_name
@_ddb_supports_patterns
class AmazonDynamoDbDeleteItem(IntegrationPattern):
    _required_fields = (
        RequiredValue("Item", "Amazon DynamoDB DeleteItem Task requires a key value"),
        RequiredValue("TableName", "Amazon DynamoDB DeleteItem Task requires a table value"),
    )
    _resource_name = ServiceArn.DYNAMODB_DELETE_ITEM

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html#API_DeleteItem_RequestParameters


@attr.s(eq=False)
@_ddb_write_attributes
@_ddb_key
@_ddb_table_name
@_ddb_supports_patterns
class AmazonDynamoDbUpdateItem(IntegrationPattern):
    _required_fields = (
        RequiredValue("Item", "Amazon DynamoDB UpdateItem Task requires a key value"),
        RequiredValue("TableName", "Amazon DynamoDB UpdateItem Task requires a table value"),
    )
    _resource_name = ServiceArn.DYNAMODB_UPDATE_ITEM

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html#API_UpdateItem_RequestParameters

    AttributeUpdates = attr.ib(default=None)
    UpdateExpression = attr.ib(default=None)
