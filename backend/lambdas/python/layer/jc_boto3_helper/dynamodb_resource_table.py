import os, sys
from boto3 import resource
from jc_custom_utilities.logger import logger_config
from dotenv import load_dotenv
from mypy_boto3_dynamodb.service_resource import Table, DynamoDBServiceResource
from mypy_boto3_dynamodb.type_defs import (
    GetItemInputTableGetItemTypeDef,
    ScanInputRequestTypeDef,
)
from typing import Optional

# load env variable
load_dotenv()

# Setup logger config
logger = logger_config(__name__)


class DynamoDBResourceTable:
    """
    Initialize the DynamoDB resource table with the specified table name and region.
        :param [Required] table_name: Name of the DynamoDB table.
        :param [Optional] region: AWS region where the table is hosted. Defaults to the AWS configuration if None.
    """

    def __init__(
        self, table_name: str, region: Optional[str] = os.getenv("DEFAULT_AWS_REGION")
    ) -> None:
        self.resource: DynamoDBServiceResource = resource(
            "dynamodb", region_name=region
        )
        self.table_name = table_name
        self.table: Table = self.resource.Table(self.table_name)

    def scan(self, **kwargs: ScanInputRequestTypeDef) -> Optional[dict]:
        """
        Defines the input parameters for a DynamoDB Scan operation.

        Boto3-stub API documentation:
        [DynamoDBServiceResource Scan](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/type_defs/#scaninputtablescantypedef)

        Attributes:
            IndexName (Optional[str]):
                The name of a secondary index to scan, if you want to scan an index instead of the table.
            TableName (Optional[str]):
                The name of the table to scan. This parameter is required only when IndexName is specified.
            AttributesToGet (Optional[List[str]]):
                List of attributes to retrieve. If not specified, all attributes will be returned.
            Limit (Optional[int]):
                The maximum number of items to evaluate (not necessarily the number of matching items).
                If DynamoDB processes the number of items up to the limit while processing the results,
                it stops the operation and returns the matching values up to that point.
            Select (Optional[Literal["ALL_ATTRIBUTES", "ALL_PROJECTED_ATTRIBUTES", "SPECIFIC_ATTRIBUTES", "COUNT"]]):
                The attributes to be returned in the result. Options include all attributes, all projected
                attributes, specific attributes, or just a count of matching items.
            ScanFilter (Optional[Dict[str, ConditionTypeDef]]):
                A condition to apply to the scan operation. Each condition is evaluated against an attribute.
            ConditionalOperator (Optional[Literal["AND", "OR"]]):
                This logical operator is used to combine multiple scan conditions.
            ExclusiveStartKey (Optional[Dict[str, Any]]):
                The primary key of the first item that this operation will evaluate. Use the value that was
                returned for `LastEvaluatedKey` in the previous operation.
            ReturnConsumedCapacity (Optional[Literal["INDEXES", "TOTAL", "NONE"]]):
                Determines the level of detail about provisioned throughput consumption that is returned.
            ProjectionExpression (Optional[str]):
                A string that identifies one or more attributes to retrieve from the table.
            FilterExpression (Optional[str]):
                A condition that DynamoDB applies after the scan operation. This filter is applied only after
                the entire table is scanned.
            ExpressionAttributeNames (Optional[Dict[str, str]]):
                One or more substitution tokens for attribute names in an expression.
            ExpressionAttributeValues (Optional[Dict[str, Any]]):
                One or more values that can be substituted in an expression.
        """

        try:
            response: dict = self.table.scan(**kwargs)

            return {
                "Items": response.get("Items", []),
                "Count": response.get("Count", 0),
            }

        except Exception as e:
            logger.error(f"{e}")
            raise ValueError(e)

    def get_item(
        self,
        **kwargs: GetItemInputTableGetItemTypeDef,
    ) -> Optional[dict]:
        """
        Defines the input parameters for a DynamoDB GetItem operation.

        Attributes:
            TableName (str):
                The name of the table from which to retrieve the item. This parameter is required.
            Key (Dict[str, Any]):
                A map of attribute names to `AttributeValue` objects, representing the primary key of the item
                to retrieve. This parameter is required.
            AttributesToGet (Optional[List[str]]):
                A list of attribute names to retrieve. If not specified, all attributes will be returned.
                Deprecated: use `ProjectionExpression` instead.
            ConsistentRead (Optional[bool]):
                If set to `True`, the operation uses strongly consistent reads; otherwise, it uses eventually
                consistent reads. The default is `False`.
            ReturnConsumedCapacity (Optional[Literal["INDEXES", "TOTAL", "NONE"]]):
                Determines the level of detail about provisioned throughput consumption that is returned.
            ProjectionExpression (Optional[str]):
                A string that identifies one or more attributes to retrieve from the table. Use this parameter
                in place of `AttributesToGet`.
            ExpressionAttributeNames (Optional[Dict[str, str]]):
                A dictionary of substitution tokens for attribute names in an expression, used to avoid reserved
                words or special characters in DynamoDB.
        """
        key = kwargs.get("Key")

        if not key:
            raise ValueError(
                "The 'key' parameter must be provided and cannot be empty."
            )

        try:
            response: dict = self.table.get_item(**kwargs)

            logger.debug(response)

            return {"Item": response.get("Item")}

        except Exception as e:
            logger.error(f"{e} - {key}")
            raise ValueError(e)
