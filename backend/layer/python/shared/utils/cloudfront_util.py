import datetime
import os

from dotenv import load_dotenv
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner
from secrets_manager_util import SecretManagerUtil
from dynamodb_util import DynamoDBResourceUtil

load_dotenv()

class CloudFrontSignerService:
    def __init__(self) -> None:
        pass

    def rsa_signer(self, message):
        secret_manager_util = SecretManagerUtil()

        private_key = serialization.load_pem_private_key(
            secret_manager_util.get_secret(os.getenv('CF_PRIVATE_KEY_SECRET_NAME')),
            password=None,
            backend=default_backend()
        )

        return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())

    def generate_signed_url(self, media_id: str, expiration_in_seconds: int):
        ddb_resource_util = DynamoDBResourceUtil()
        metadata = ddb_resource_util.get_media_metadata(media_id)

        content_url = f'{os.getenv('CLOUDFRONT_DOMAIN')}{metadata['s3_key']}'
        
        expiration_time = datetime.datetime.now() + datetime.timedelta(seconds=expiration_in_seconds)

        cloudfront_signer = CloudFrontSigner(os.getenv('CF_PUBLIC_KEY_ID'), self.rsa_signer)

        signed_url = cloudfront_signer.generate_presigned_url(
            url=content_url,
            date_less_than=expiration_time
        )

        return signed_url
    
cfsigner = CloudFrontSignerService()

print(cfsigner.generate_signed_url('abc123', 3600))
