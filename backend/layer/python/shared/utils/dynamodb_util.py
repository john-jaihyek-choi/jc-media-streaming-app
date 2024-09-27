import boto3
import os

from dotenv import load_dotenv
from mypy_boto3_dynamodb.service_resource import Table

load_dotenv()


class DynamoDBResourceUtil:
    def __init__(self, region: str = os.getenv("AWS_REGION", "us-east-2")) -> None:
        self.table: Table = boto3.resource("dynamodb", region_name=region).Table(
            os.getenv("METADATA_DDB_TABLE_NAME")
        )

    def get_media_metadata(self, media_id: str):

        response = self.table.get_item(Key={"id": media_id})

        return response.get("Item", {})
