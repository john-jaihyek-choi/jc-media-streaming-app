import os, sys

if os.getenv("AWS_EXECUTION_ENV"):
    sys.path.append("/opt/python")

import boto3, json
from dotenv import load_dotenv
from layer.utils.logger import logger_config
from mypy_boto3_secretsmanager.client import SecretsManagerClient
from mypy_boto3_secretsmanager.type_defs import (
    GetSecretValueRequestRequestTypeDef,
    GetSecretValueResponseTypeDef,
)
from botocore.exceptions import ClientError
from typing import Optional

# Load env variable
load_dotenv()

# Setup logger config
logger = logger_config(__name__)


class SecretManager:
    def __init__(self, region: Optional[str]) -> None:
        """
        :param region: AWS region where Secrets Manager is hosted. Defaults to 'us-east-2'.
        """
        self.client: SecretsManagerClient = boto3.client(
            "secretsmanager", region_name=region
        )

    def get_secret_value(
        self,
        **kwargs: GetSecretValueRequestRequestTypeDef,
    ) -> Optional[bytes]:
        secret_id = kwargs["SecretId"]

        if not secret_id:
            raise ValueError(
                "The 'SecretId' parameter must be provided and cannot be empty."
            )

        try:
            response: GetSecretValueResponseTypeDef = self.client.get_secret_value(
                SecretId=secret_id, **kwargs
            )

            logger.info("secret string retrieval successful")

            return json.dumps(response, indent=4)

        except ClientError as e:
            logger.error(f"ClientError occurred: {e.response['Error']}")
            raise RuntimeError("An AWS service client error occurred.")
        except Exception as e:
            # Catch-all for any other unexpected exceptions
            logger.error(f"An unexpected error occurred: {str(e)}")
            raise RuntimeError("An unexpected AWS service error occurred.")


secretManager = SecretManager("us-east-2")
secretManager.get_secret_value(SecretId=os.getenv("CF_PRIVATE_KEY_SECRET_ID"))
