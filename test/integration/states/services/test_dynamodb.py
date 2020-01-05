"""Integration tests for ``rhodes.states.services.ecs``."""
import pytest

from rhodes.states.services.dynamodb import AmazonDynamoDb
from rhodes.structures import Parameters

from ...integration_test_utils import build_and_try_single_step_state_machine

pytestmark = [pytest.mark.integ]


@pytest.fixture
def table() -> AmazonDynamoDb:
    yield AmazonDynamoDb(TableName="foo")


def test_ddb_get_item_minimal(table: AmazonDynamoDb):
    step = table.get_item("test", Key=dict(foo="bar"))
    build_and_try_single_step_state_machine(step)


def test_ddb_get_item_all_specials(table: AmazonDynamoDb):
    step = table.get_item(
        "test",
        Key=dict(foo="bar"),
        AttributesToGet=["foo", "bar"],
        ConsistentRead=True,
        ExpressionAttributeNames=Parameters(foo="bar"),
        ProjectionExpression="foo",
        ReturnConsumedCapacity="bar",
    )
    build_and_try_single_step_state_machine(step)


_WRITE_SPECIALS_KWARGS = dict(
    ConditionalOperator="foo",
    ConditionExpression="bar",
    Expected=Parameters(foo=dict(AttributeValueList=[dict(BOOL=False)])),
    ExpressionAttributeNames=Parameters(foo="bar"),
    ExpressionAttributeValues=Parameters(foo=dict(BOOL=False)),
    ReturnConsumedCapacity="foo",
    ReturnItemCollectionMetrics="bar",
    ReturnValues="baz",
)


def test_ddb_put_item_minimal(table: AmazonDynamoDb):
    step = table.put_item("test", Item=Parameters(foo="bar", baz="wow"))
    build_and_try_single_step_state_machine(step)


def test_ddb_put_item_all_specials(table: AmazonDynamoDb):
    step = table.put_item("test", Item=Parameters(foo="bar", baz="wow"), **_WRITE_SPECIALS_KWARGS)
    build_and_try_single_step_state_machine(step)


def test_ddb_delete_item_minimal(table: AmazonDynamoDb):
    step = table.delete_item("test", Key=Parameters(foo="bar", baz="wow"))
    build_and_try_single_step_state_machine(step)


def test_ddb_delete_item_all_specials(table: AmazonDynamoDb):
    step = table.delete_item("test", Key=Parameters(foo="bar", baz="wow"), **_WRITE_SPECIALS_KWARGS)
    build_and_try_single_step_state_machine(step)


def test_ddb_update_item_minimal(table: AmazonDynamoDb):
    step = table.update_item("test", Key=Parameters(foo="bar", baz="wow"))
    build_and_try_single_step_state_machine(step)


def test_ddb_update_item_all_specials(table: AmazonDynamoDb):
    step = table.update_item("test", Key=Parameters(foo="bar", baz="wow"), **_WRITE_SPECIALS_KWARGS)
    build_and_try_single_step_state_machine(step)
