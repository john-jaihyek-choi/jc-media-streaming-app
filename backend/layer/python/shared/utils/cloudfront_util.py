import datetime
from dotenv import load_dotenv

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner
from secrets_manager_util import SecretManagerUtil

load_dotenv()

class CloudFrontSignerService:
    def __init__(self) -> None:
        self.pem_key = SecretManagerUtil.get_secret('secret-name')

    def rsa_signer(self, message):
        private_key = serialization.load_pem_private_key(
            self.pem_key,
            password=None,
            backend=default_backend()
        )

        return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())

    def generate_signed_url(self, media_id, content_url, public_key_id, expiration_in_seconds):
        expiration_time = datetime.datetime.now() + datetime.timedelta(seconds=expiration_in_seconds)

        cloudfront_signer = CloudFrontSigner(public_key_id, self.rsa_signer)

        signed_url = cloudfront_signer.generate_presigned_url(
            url=content_url,
            date_less_than=expiration_time
        )

        return signed_url