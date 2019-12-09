"""Amazon DynamoDB Integrations for Task states.

https://docs.aws.amazon.com/step-functions/latest/dg/connect-ddb.html
"""
import attr
from attr.validators import instance_of

from rhodes._util import RHODES_ATTRIB, RequiredValue
from rhodes.identifiers import IntegrationPattern, ServiceArn
from rhodes.states.services import ServiceIntegration
from rhodes.states.services.util import supports_patterns

__all__ = (
    "AmazonDynamoDb",
    "AmazonDynamoDbGetItem",
    "AmazonDynamoDbPutItem",
    "AmazonDynamoDbDeleteItem",
    "AmazonDynamoDbUpdateItem",
)

_ddb_supports_patterns = supports_patterns(IntegrationPattern.REQUEST_RESPONSE)


@attr.s
class AmazonDynamoDb:
    TableName = RHODES_ATTRIB(validator=instance_of(str))

    def get_item(self, **kwargs):
        return AmazonDynamoDbGetItem(TableName=self.TableName, **kwargs)

    def put_item(self, **kwargs):
        return AmazonDynamoDbPutItem(TableName=self.TableName, **kwargs)

    def delete_item(self, **kwargs):
        return AmazonDynamoDbDeleteItem(TableName=self.TableName, **kwargs)

    def update_item(self, **kwargs):
        return AmazonDynamoDbUpdateItem(TableName=self.TableName, **kwargs)


def _ddb_table_name(cls: ServiceIntegration) -> ServiceIntegration:
    cls.TableName = RHODES_ATTRIB()

    return cls


def _ddb_key(cls: ServiceIntegration) -> ServiceIntegration:
    cls.Key = RHODES_ATTRIB()

    return cls


def _ddb_write_attributes(cls: ServiceIntegration) -> ServiceIntegration:
    cls.ConditionalOperator = RHODES_ATTRIB()
    cls.ConditionExpression = RHODES_ATTRIB()
    cls.Expected = RHODES_ATTRIB()
    cls.ExpressionAttributeNames = RHODES_ATTRIB()
    cls.ExpressionAttributeValues = RHODES_ATTRIB()
    cls.ReturnConsumedCapacity = RHODES_ATTRIB()
    cls.ReturnItemCollectionMetrics = RHODES_ATTRIB()
    cls.ReturnValues = RHODES_ATTRIB()

    return cls


@attr.s(eq=False)
@_ddb_key
@_ddb_table_name
@_ddb_supports_patterns
class AmazonDynamoDbGetItem(ServiceIntegration):
    _required_fields = (
        RequiredValue("Key", "Amazon DynamoDB GetItem Task requires a key value"),
        RequiredValue("TableName", "Amazon DynamoDB GetItem Task requires a table value"),
    )
    _resource_name = ServiceArn.DYNAMODB_GET_ITEM

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html#DDB-GetItem-request-Key

    AttributesToGet = RHODES_ATTRIB()
    ConsistentRead = RHODES_ATTRIB()
    ExpressionAttributeNames = RHODES_ATTRIB()
    ProjectionExpression = RHODES_ATTRIB()
    ReturnConsumedCapacity = RHODES_ATTRIB()


@attr.s(eq=False)
@_ddb_write_attributes
@_ddb_table_name
@_ddb_supports_patterns
class AmazonDynamoDbPutItem(ServiceIntegration):
    _required_fields = (
        RequiredValue("Item", "Amazon DynamoDB PutItem Task requires an item value"),
        RequiredValue("TableName", "Amazon DynamoDB PutItem Task requires a table value"),
    )
    _resource_name = ServiceArn.DYNAMODB_PUT_ITEM

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html#DDB-PutItem-request-Item

    Item = RHODES_ATTRIB()


@attr.s(eq=False)
@_ddb_write_attributes
@_ddb_key
@_ddb_table_name
@_ddb_supports_patterns
class AmazonDynamoDbDeleteItem(ServiceIntegration):
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
class AmazonDynamoDbUpdateItem(ServiceIntegration):
    _required_fields = (
        RequiredValue("Item", "Amazon DynamoDB UpdateItem Task requires a key value"),
        RequiredValue("TableName", "Amazon DynamoDB UpdateItem Task requires a table value"),
    )
    _resource_name = ServiceArn.DYNAMODB_UPDATE_ITEM

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html#API_UpdateItem_RequestParameters

    AttributeUpdates = RHODES_ATTRIB()
    UpdateExpression = RHODES_ATTRIB()
