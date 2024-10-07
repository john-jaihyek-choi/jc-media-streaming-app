import boto3
import logging
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.service_resource import Table
from mypy_boto3_dynamodb.type_defs import (
    GetItemOutputTableTypeDef,
    GetItemInputTableGetItemTypeDef,
)
from typing import Optional

# load env variable
load_dotenv()

# Set up logger
logger = logging.getLogger(__name__)


class DynamoDBResourceTable:
    def __init__(
        self, table_name: str, region: Optional[str] = os.getenv("DEFAULT_AWS_REGION")
    ) -> None:
        """
        Initialize the DynamoDB resource table with the specified table name and region.
            :param [Required] table_name: Name of the DynamoDB table.
            :param region: AWS region where the table is hosted. Defaults to the AWS configuration if None.
        """
        self.table_name = table_name
        self.region = region

        try:
            self.table: Table = boto3.resource(
                "dynamodb", region_name=self.region
            ).Table(self.table_name)

            logger.info(
                f"Connected to DynamoDB table: {self.table_name} in region: {self.region}"
            )
        except ClientError as e:
            logger.error(f"Failed to connect to DynamoDB table {self.table_name}: {e}")
            raise RuntimeError(
                f"Could not connect to DynamoDB table {self.table_name}"
            ) from e

    def get_item(
        self,
        **kwargs: GetItemInputTableGetItemTypeDef,
    ) -> Optional[GetItemOutputTableTypeDef]:
        """
        Retrieve an item from the DynamoDB table by key.
            :param [Required] (dict) Key: Primary key of the item to retrieve.
            :param [Optional] (list[string]) AttributesToGet: List of attributes to retrieve.
            :param [Optional] (bool) ConsistentRead: Whether to perform a consistent read.
            :param [Optional] ("INDEXES" | "TOTAL" | "NONE") ReturnConsumedCapacity: Return the consumed capacity units.
            :param [Optional] (string) ProjectionExpression: A string that identifies the attributes you want.
            :param [Optional] (dict) ExpressionAttributeNames: Substitution tokens for attribute names in an expression.
            :return The retrieved item or None if not found
        """
        if "Key" not in kwargs:
            raise ValueError(
                "The 'key' parameter must be provided and cannot be empty."
            )

        try:
            response: GetItemOutputTableTypeDef = self.table.get_item(**kwargs)

            return response

        except ClientError as e:
            logger.error(f"Failed to retrieve item from {self.table_name}: {e}")
            raise RuntimeError(
                f"Failed to retrieve item: {e.response['Error']['Message']}"
            ) from e

        except Exception as e:
            logger.error(
                f"Unexpected error when retrieving item {kwargs['Key']} from table {self.table_name}: {e}"
            )
            raise
