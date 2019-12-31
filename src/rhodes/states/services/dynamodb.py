"""
`Amazon DynamoDB <https://docs.aws.amazon.com/step-functions/latest/dg/connect-ddb.html>`_ Task states.
"""
import attr
from attr.validators import instance_of

from rhodes._types import StateMirror
from rhodes._util import RHODES_ATTRIB, RequiredValue, docstring_with_param
from rhodes.identifiers import IntegrationPattern, ServiceArn
from rhodes.states import State
from rhodes.states.services._util import service_integration

__all__ = (
    "AmazonDynamoDb",
    "AmazonDynamoDbGetItem",
    "AmazonDynamoDbPutItem",
    "AmazonDynamoDbDeleteItem",
    "AmazonDynamoDbUpdateItem",
)

_ddb_service_integration = service_integration(IntegrationPattern.REQUEST_RESPONSE)


@attr.s
class AmazonDynamoDb:
    """Helper to provide easy access to integration helpers.

    :param TableName: The table to interact with
    """

    TableName = RHODES_ATTRIB(validator=instance_of(str))

    def get_item(self, **kwargs) -> "AmazonDynamoDbGetItem":
        return AmazonDynamoDbGetItem(TableName=self.TableName, **kwargs)

    def put_item(self, **kwargs) -> "AmazonDynamoDbPutItem":
        return AmazonDynamoDbPutItem(TableName=self.TableName, **kwargs)

    def delete_item(self, **kwargs) -> "AmazonDynamoDbDeleteItem":
        return AmazonDynamoDbDeleteItem(TableName=self.TableName, **kwargs)

    def update_item(self, **kwargs) -> "AmazonDynamoDbUpdateItem":
        return AmazonDynamoDbUpdateItem(TableName=self.TableName, **kwargs)


def _ddb_table_name(cls: StateMirror) -> StateMirror:
    cls.TableName = RHODES_ATTRIB()
    cls.__doc__ = docstring_with_param(cls, "TableName", description="The table to interact with")

    return cls


def _ddb_key(cls: StateMirror) -> StateMirror:
    cls.Key = RHODES_ATTRIB()
    cls.__doc__ = docstring_with_param(
        cls,
        "Key",
        description=(
            "A map of attribute names to AttributeValue objects, representing the primary key of the item to retrieve."
        ),
    )

    return cls


def _ddb_write_attributes(cls: StateMirror) -> StateMirror:
    cls.ConditionalOperator = RHODES_ATTRIB()
    cls.__doc__ = docstring_with_param(
        cls,
        "ConditionalOperator",
        description=(
            "This is a legacy parameter. "
            "Use ConditionExpression instead. "
            "For more information, see ConditionalOperator in the Amazon DynamoDB Developer Guide."
        ),
    )

    cls.ConditionExpression = RHODES_ATTRIB()
    cls.__doc__ = docstring_with_param(
        cls,
        "ConditionExpression",
        description="A condition that must be satisfied in order for a conditional operation to succeed.",
    )

    cls.Expected = RHODES_ATTRIB()
    cls.__doc__ = docstring_with_param(
        cls,
        "Expected",
        description=(
            "This is a legacy parameter. "
            "Use ConditionExpression instead. "
            "For more information, see Expected in the Amazon DynamoDB Developer Guide."
        ),
    )

    cls.ExpressionAttributeNames = RHODES_ATTRIB()
    cls.__doc__ = docstring_with_param(
        cls,
        "ExpressionAttributeNames",
        description="One or more substitution tokens for attribute names in an expression.",
    )

    cls.ExpressionAttributeValues = RHODES_ATTRIB()
    cls.__doc__ = docstring_with_param(
        cls, "ExpressionAttributeValues", description="One or more values that can be substituted in an expression."
    )

    cls.ReturnConsumedCapacity = RHODES_ATTRIB()
    cls.__doc__ = docstring_with_param(
        cls,
        "ReturnConsumedCapacity",
        description=(
            "Determines the level of detail about provisioned throughput consumption that is returned in the response"
        ),
    )

    cls.ReturnItemCollectionMetrics = RHODES_ATTRIB()
    cls.__doc__ = docstring_with_param(
        cls, "ReturnItemCollectionMetrics", description="Determines whether item collection metrics are returned."
    )

    cls.ReturnValues = RHODES_ATTRIB()
    cls.__doc__ = docstring_with_param(
        cls,
        "ReturnValues",
        description=(
            "Use ReturnValues if you want to get the item attributes "
            "as they appeared before they were updated with the request."
        ),
    )

    return cls


@attr.s(eq=False)
@_ddb_key
@_ddb_table_name
@_ddb_service_integration
class AmazonDynamoDbGetItem(State):
    """
    :param AttributesToGet: This is a legacy parameter. Use ProjectionExpression instead.
       For more information, see AttributesToGet in the Amazon DynamoDB Developer Guide.
    :param ConsistentRead: Determines the read consistency model
    :param ExpressionAttributeNames: One or more substitution tokens for attribute names in an expression.
    :param ProjectionExpression: A string that identifies one or more attributes to retrieve from the table.
    :param ReturnConsumedCapacity: Determines the level of detail about provisioned throughput consumption
       that is returned in the response
    """

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
@_ddb_service_integration
class AmazonDynamoDbPutItem(State):
    """
    :param Item: A map of attribute name/value pairs, one for each attribute.
    """

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
@_ddb_service_integration
class AmazonDynamoDbDeleteItem(State):
    """"""

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
@_ddb_service_integration
class AmazonDynamoDbUpdateItem(State):
    """
    :param AttributeUpdates: This is a legacy parameter. Use UpdateExpression instead.
       For more information, see AttributeUpdates in the Amazon DynamoDB Developer Guide.
    :param UpdateExpression: An expression that defines one or more attributes to be updated,
       the action to be performed on them, and new values for them.
    """

    _required_fields = (
        RequiredValue("Item", "Amazon DynamoDB UpdateItem Task requires a key value"),
        RequiredValue("TableName", "Amazon DynamoDB UpdateItem Task requires a table value"),
    )
    _resource_name = ServiceArn.DYNAMODB_UPDATE_ITEM

    # TODO: Sort out validation rules
    #  https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html#API_UpdateItem_RequestParameters

    AttributeUpdates = RHODES_ATTRIB()
    UpdateExpression = RHODES_ATTRIB()
