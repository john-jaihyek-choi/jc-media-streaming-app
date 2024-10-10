import os, sys
import boto3
from dotenv import load_dotenv
from utils.logger import logger_config
from mypy_boto3_secretsmanager.client import SecretsManagerClient
from mypy_boto3_secretsmanager.type_defs import (
    GetSecretValueRequestRequestTypeDef,
)
from botocore.exceptions import ClientError
from typing import Optional

# Load env variable
load_dotenv()

# Setup logger config
logger = logger_config(__name__)


class SecretsManager:
    """
    :param region: AWS region where the target secret is hosted. Defaults to 'us-east-2'.
    """

    def __init__(self, region: Optional[str] = os.getenv("DEFAULT_AWS_REGION")) -> None:
        self.client: SecretsManagerClient = boto3.client(
            "secretsmanager", region_name=region
        )

    def get_secret_value(
        self,
        **kwargs: GetSecretValueRequestRequestTypeDef,
    ) -> Optional[bytes]:
        """
        Defines the input parameters for retrieving a secret value from AWS Secrets Manager.

        Attributes:
            SecretId (str):
                The identifier for the secret from which to retrieve the value. This can be the secret name,
                Amazon Resource Name (ARN), or the unique identifier of the secret. This parameter is required.
            VersionId (Optional[str]):
                The unique identifier of the version of the secret to retrieve. If not specified, AWS Secrets Manager
                retrieves the version marked with the 'AWSCURRENT' label by default.
            VersionStage (Optional[str]):
                The staging label of the version of the secret to retrieve. By default, AWS Secrets Manager uses
                'AWSCURRENT' if not provided.
        """
        secret_id = kwargs.get("SecretId")

        if not secret_id:
            raise ValueError(
                "The 'SecretId' parameter must be provided and cannot be empty."
            )

        try:
            response: dict = self.client.get_secret_value(**kwargs)

            secret = response.get("SecretString")

            logger.info("secret string retrieval successful")

            return {
                "SecretString": (
                    secret.encode("utf-8") if isinstance(secret, str) else secret
                )
            }

        except ClientError as e:
            logger.error(f"ClientError occurred: {e.response['Error']}")
            raise RuntimeError("An AWS service client error occurred.")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            raise RuntimeError("An unexpected AWS service error occurred.")
