import boto3
import logging
from mypy_boto3_secretsmanager.client import SecretsManagerClient
from mypy_boto3_secretsmanager.type_defs import GetSecretValueResponseTypeDef
from botocore.exceptions import ClientError
from typing import Optional


# Set up logging
logger = logging.getLogger(__name__)


class SecretManagerHelper:
    def __init__(self, region: Optional[str]) -> None:
        """
        :param region: AWS region where Secrets Manager is hosted. Defaults to 'us-east-2'.
        """
        self.region = region
        self.client: SecretsManagerClient = boto3.client(
            "secretsmanager", region_name=region
        )

    def get_secret(
        self,
        secret_id: str,
        version_id: Optional[str] = None,
        version_stage: Optional[str] = None,
    ) -> Optional[bytes]:
        if not secret_id:
            raise ValueError(f"secret_id is a required field.")

        try:
            response: GetSecretValueResponseTypeDef = self.client.get_secret_value(
                SecretId=secret_id, VersionId=version_id, VersionStage=version_stage
            )

            if "SecretString" not in response:
                KeyError(f"SecretString not found for SecretId: {secret_id}")

            secret = response["SecretString"]

            return secret.encode("utf-8") if isinstance(secret, str) else secret

        except ClientError as e:
            logger.error(f"Failed to retrieve secret for secret_id {secret_id}: {e}")

            raise RuntimeError(
                f"Failed to retrieve secret: {e.response['Error']['Message']}"
            ) from e
