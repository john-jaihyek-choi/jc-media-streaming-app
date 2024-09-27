import boto3
import logging
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.service_resource import Table
from mypy_boto3_dynamodb.type_defs import GetItemOutputTableTypeDef
from typing import Optional, Dict, Any


# Set up logger
logger = logging.getLogger(__name__)


class DynamoDBResourceTable:
    def __init__(self, table_name: str, region: str) -> None:
        """
        Initialize the DynamoDB resource table with the specified table name and region.
            :param table_name: Name of the DynamoDB table.
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
        key: Dict[str, Any],
        attributes_to_get: Optional[list] = None,
        consistent_read: Optional[bool] = None,
        return_consumed_capacity: Optional[str] = None,
        projection_expression: Optional[str] = None,
        expression_attribute_names: Optional[Dict[str, str]] = None,
    ) -> Optional[GetItemOutputTableTypeDef]:
        """
        Retrieve an item from the DynamoDB table by key.
            :param key: Primary key of the item to retrieve.
            :param attributes_to_get: List of attributes to retrieve.
            :param consistent_read: Whether to perform a consistent read.
            :param return_consumed_capacity: Return the consumed capacity units.
            :param projection_expression: A string that identifies the attributes you want.
            :param expression_attribute_names: Substitution tokens for attribute names in an expression.
        """
        if not key:
            raise ValueError(
                "The 'key' parameter must be provided and cannot be empty."
            )

        try:
            response: GetItemOutputTableTypeDef = self.table.get_item(
                Key=key,
                AttributesToGet=attributes_to_get,
                ConsistentRead=consistent_read,
                ReturnConsumedCapacity=return_consumed_capacity,
                ProjectionExpression=projection_expression,
                ExpressionAttributeNames=expression_attribute_names,
            )

            return response

        except ClientError as e:
            logger.error(f"Failed to retrieve item from {self.table_name}: {e}")
            raise RuntimeError(
                f"Failed to retrieve item: {e.response['Error']['Message']}"
            ) from e

        except Exception as e:
            logger.error(
                f"Unexpected error when retrieving item {key} from table {self.table_name}: {e}"
            )
            raise
