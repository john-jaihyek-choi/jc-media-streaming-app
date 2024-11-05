import os, pytest
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock
from jc_boto3_helper.cloudfront_signer import CloudFrontSigner
from jc_boto3_helper.secrets_manager import SecretsManager
from jc_custom_utilities.logger import logger_config

# Load env variable
load_dotenv()

# Setup logger config
logger = logger_config(__name__)

public_key_id = "CF_PUBLIC_KEY_ID"
pem_key = b"PEM KEY"
cf_signer = CloudFrontSigner(public_key_id, pem_key)


class TestCloudFrontSigner:
    def test_initialization_success(self):
        global pem_key
        global public_key_id

        assert cf_signer.public_key_id == public_key_id
        assert cf_signer.pem_key == pem_key

    def test_initialization_missing_arguments(self):
        with pytest.raises(TypeError):
            CloudFrontSigner("", pem_key)
        with pytest.raises(TypeError):
            CloudFrontSigner(public_key_id, None)

    def test_generate_presigned_url_success(self):
        url = "https://example.com/test"
        expiration_in_seconds = 3600

        with patch.object(
            cf_signer, "generate_presigned_url", return_value={"url": "signed_url"}
        ) as mock_generate_presigned_url:
            signed_url = cf_signer.generate_presigned_url(url, expiration_in_seconds)

            assert signed_url["url"] == "signed_url"
            mock_generate_presigned_url.assert_called_once()

    def test_generate_presigned_url_missing_url(cloudfront_signer):
        with pytest.raises(TypeError):
            cf_signer.generate_presigned_url("", 3600)

    def test_generate_presigned_url_invalid_string_expiration(cloudfront_signer):
        with pytest.raises(TypeError):
            cf_signer.generate_presigned_url("https://example.com/test", "invalid")

    def test_generate_presigned_url_missing_expiration(cloudfront_signer):
        with pytest.raises(TypeError):
            cf_signer.generate_presigned_url("https://example.com/test", None)
