import datetime
import os
import validators
import logging
from dotenv import load_dotenv
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner
from botocore.exceptions import ClientError
from custom.exceptions import InvalidSignedUrlError
from typing import Optional

# Set up logger
logger = logging.getLogger(__name__)

load_dotenv()


class CloudFrontSignerHelper:
    def __init__(self) -> None:
        self.pem_key: bytes | None = None

    # used exclusively for CloudFrontSignerHelper
    def _rsa_signer(self, message):
        private_key = serialization.load_pem_private_key(
            self.pem_key, password=None, backend=default_backend()
        )

        return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())

    def generate_signed_url(
        self,
        pem_key: bytes,
        public_key_id: str,
        url: str,
        expiration_in_seconds: Optional[int] = os.getenv("CF_DEFAULT_URL_EXP"),
    ) -> str:
        if not pem_key:
            raise ValueError(f"pem_key is a required field")
        elif not isinstance(pem_key, bytes):
            raise ValueError(
                f"pem_key is not of type 'bytes'. pem_key must be a valid bytes type"
            )

        self.pem_key: bytes = pem_key

        expiration_time = datetime.datetime.now() + datetime.timedelta(
            seconds=expiration_in_seconds
        )

        try:
            cloudfront_signer = CloudFrontSigner(public_key_id, self._rsa_signer)

            signed_url: str = cloudfront_signer.generate_presigned_url(
                url=url, date_less_than=expiration_time, policy=None
            )

            if not validators.url(signed_url):
                raise InvalidSignedUrlError()

            return signed_url

        except ClientError as e:
            logger.error(f"Failed to retrieve item from {self.table_name}: {e}")
            raise RuntimeError(
                f"Failed to retrieve item: {e.response['Error']['Message']}"
            ) from e
