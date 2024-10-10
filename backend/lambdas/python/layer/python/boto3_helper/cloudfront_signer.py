import os, sys
import datetime, validators
from layer.python.utils.logger import logger_config
from layer.python.utils.exceptions import InvalidSignedUrlError
from dotenv import load_dotenv
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner as cfsigner
from typing import Optional

# Load env variable
load_dotenv()

# Setup logger config
logger = logger_config(__name__)


class CloudFrontSigner:
    def __init__(self, public_key_id: str, pem_key: bytes) -> None:
        if not pem_key:
            raise TypeError("missing 1 required positional argument: 'pem_key'")
        elif not public_key_id:
            raise TypeError("missing 1 required positional argument: 'public_key_id'")
        elif not isinstance(pem_key, bytes):
            raise TypeError(
                f"pem_key is not of type 'bytes'. pem_key must be a valid bytes type. Received type(pem_key)={type(pem_key)}"
            )
        self.pem_key = pem_key
        self.public_key_id = public_key_id
        self.cloudfront_signer = cfsigner(public_key_id, self._rsa_signer)

    # used exclusively for CloudFrontSigner
    def _rsa_signer(self, message):
        private_key = serialization.load_pem_private_key(
            self.pem_key, password=None, backend=default_backend()
        )

        return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())

    def generate_presigned_url(
        self,
        url: str,
        expiration_in_seconds: int = os.getenv("CF_DEFAULT_URL_EXP"),
        policy: Optional[str] = None,
    ) -> str:
        if not url:
            raise TypeError("missing 1 required positional argument: 'url")
        elif not expiration_in_seconds:
            raise TypeError(
                "missing 1 required positional argument: 'expiration_in_seconds"
            )
        elif not isinstance(expiration_in_seconds, str) and not isinstance(
            expiration_in_seconds, int
        ):
            raise TypeError(
                f"expiration_in_seconds must be of type int. Received type {type(expiration_in_seconds)}"
            )

        try:
            expiration_time = datetime.datetime.now() + datetime.timedelta(
                seconds=int(expiration_in_seconds)
            )

            signed_url: str = self.cloudfront_signer.generate_presigned_url(
                url=url, date_less_than=expiration_time, policy=policy
            )

            # Leaving it for potential error handling in the future
            # if not validators.url(signed_url):
            #     raise InvalidSignedUrlError()

            logger.info("signed url generation successful")
            logger.debug(signed_url)

            return {"url": signed_url}

        except Exception as e:
            logger.error(f"{e}")
            raise ValueError(e)
