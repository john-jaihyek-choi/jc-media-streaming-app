import boto3
import os
import logging
from dotenv import load_dotenv
from utils.dynamodb_resource_table import DynamoDBResourceTable
from mypy_boto3_dynamodb.type_defs import GetItemOutputTableTypeDef
from botocore.exceptions import ClientError
from typing import Optional

# Setup environment variable
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)


class MediaMetadataTableHelper(DynamoDBResourceTable):
    def __init__(self, table_name: str, region: str) -> None:
        self.table_name = table_name or os.getenv("METADATA_DDB_TABLE_NAME")

        if not self.table_name:
            raise ValueError("Environment variable METADATA_DDB_TABLE_NAME is not set")

        super().__init__(table_name=self.table_name, table_name=region)

    def get_media_metadata(self, media_id: str) -> Optional[GetItemOutputTableTypeDef]:
        if not media_id:
            raise ValueError("media_id is a required field")

        try:
            response: GetItemOutputTableTypeDef = self.get_item(Key={"id": media_id})

            if "Item" not in response:
                raise KeyError(f"Metadata not found for media_id: {media_id}")

            return response

        except ClientError as e:
            logger.error(
                f"Failed to retrieve media metadata for media_id {media_id}: {e}"
            )

            raise RuntimeError(
                f"Failed to retrieve media metadata: {e.response['Error']['Message']}"
            ) from e

        except KeyError as e:
            logger.warning(f"Item with media_id {media_id} not found in table")
            raise e
