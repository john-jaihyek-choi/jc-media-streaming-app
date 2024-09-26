import boto3
import os
from botocore.client import BaseClient
from botocore.exceptions import ClientError

class SecretManagerUtil:
    def __init__(self, region: str = os.getenv('AWS_REGION', 'us-east-2')) -> None:
        """
        Initializes the Secrets Manager client.

        :param region: AWS region where Secrets Manager is hosted. Defaults to 'us-east-2'.
        """
        self.region = region
        self.client: BaseClient = boto3.client(
            service_name='secretsmanager',
            region_name=region
        )
    
    def get_secret(self, secret_name: str) -> bytes:
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            secret = response['SecretString']

            if isinstance(secret, str):
                secret = secret.encode('utf-8')

            return secret.encode('utf-8') if isinstance(secret, str) else secret
        
        except ClientError as e:
            raise Exception(f"Failed to retrieve secret: {e}")