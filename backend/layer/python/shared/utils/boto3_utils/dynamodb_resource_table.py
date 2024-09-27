import boto3
import os

from dotenv import load_dotenv
from mypy_boto3_dynamodb.service_resource import Table
from mypy_boto3_dynamodb.type_defs import GetItemInput, GetItemOutput
from boto3.dynamodb.types import Binary
from typing import Optional, Dict, Any

load_dotenv()


class DynamoDBResourceTable:
    def __init__(self, table_name: str, region: Optional[str] = None) -> None:
        self.table: Table = boto3.resource(
            "dynamodb", region_name=region or os.getenv("AWS_REGION")
        ).Table()

    def get_item(
        self,
        key: Dict[str, Any],
        attributes_to_get: Optional[list],
        consistent_read: Optional[bool],
        return_consumed_capacity: Optional[str],
        ProjectionExpression: Optional[str],
        ExpressionAttributeNames: Optional[Dict[str, str]],
    ) -> GetItemOutput:

        response: GetItemOutput = self.table.get_item(
            key, attributes_to_get, consistent_read, return_consumed_capacity
        )

        return response.get("Item", {})
