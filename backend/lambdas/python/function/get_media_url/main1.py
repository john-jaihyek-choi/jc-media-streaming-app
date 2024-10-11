import os, json, sys
from dotenv import load_dotenv
from http import HTTPStatus
from jc_boto3_helper.cloudfront_signer import CloudFrontSigner
from jc_boto3_helper.secrets_manager import SecretsManager
from jc_boto3_helper.dynamodb_resource_table import DynamoDBResourceTable
from jc_custom_utilities.logger import logger_config
from jc_custom_utilities.functions import generate_api_response
from jc_custom_utilities.types import HTTPMethod
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from aws_lambda_powertools.utilities.typing import LambdaContext

# Load env variable
load_dotenv()

# Setup logger config
logger = logger_config(__name__)

# instantiate secrets manager client globally
secrets_manager = SecretsManager(os.getenv("DEFAULT_AWS_REGION"))

# instantiate ddb resource client globally
ddb_table = DynamoDBResourceTable(os.getenv("METADATA_DDB_TABLE_NAME"))


def handler(event: APIGatewayProxyEvent, context: LambdaContext):
    logger.debug(event)

    path_parameters: dict = event.get("pathParameters", {})

    # check for missing media_id parameter
    if path_parameters and "media-id" in path_parameters:
        url = make_url(media_id=path_parameters.get("media-id"))

        if url is None:
            return generate_api_response(
                status_code=HTTPStatus.NOT_FOUND,
                body={"error": "Media not found."},
            )

        logger.debug(f"media url - {url}")
    else:
        logger.error(f"Invalid request")

        return generate_api_response(
            status_code=HTTPStatus.BAD_REQUEST,
            body={"error": "Invalid request. Please provide a valid request"},
        )

    return get_presigned_url(url)


def make_url(media_id: str):
    try:
        ddb_response: dict = ddb_table.get_item(
            Key={"id": media_id}, ProjectionExpression="s3_key"
        )

        logger.debug(ddb_response)

        item: dict = ddb_response.get("Item")

        if not item or "s3_key" not in item:
            return

        s3_key: str = item.get("s3_key")
        url = os.getenv("CLOUDFRONT_DOMAIN") + s3_key

        logger.debug(f"concatenated domain and s3_key - {url}")

        return url

    except Exception as e:
        logger.error(f"An error occurred while fetching the URL: {e}")
        return


def get_presigned_url(url: str):
    global secrets_manager

    try:
        # get pem_key using secret id of the private key
        secret: dict = secrets_manager.get_secret_value(
            SecretId=os.getenv("CF_PRIVATE_KEY_SECRET_ID")
        )
        pem_key: bytes = secret.get("SecretString")

        # instantiate cf_signer - Note: instantiated in this function scope for best security practice
        cf_signer = CloudFrontSigner(
            public_key_id=os.getenv("CF_PUBLIC_KEY_ID"), pem_key=pem_key
        )

        # generate a presigned url of the media
        cf_signer_response = cf_signer.generate_presigned_url(
            url=url,
            expiration_in_seconds=os.getenv("CF_DEFAULT_URL_EXP", 3600),
        )

        logger.info("presigned url retrieval successful")
        logger.debug(cf_signer_response)

        status_code = HTTPStatus.OK
        body = cf_signer_response

    except Exception as e:
        status_code = HTTPStatus.BAD_REQUEST
        body = {"message": f"{e}"}

    finally:
        # format/generate api response and return
        return generate_api_response(status_code=status_code, body=body)


url = handler(
    {
        "resource": "/media/{media-id}/presigned-url",
        "path": "/media/abc123/presigned-url",
        "httpMethod": "POST",
        "headers": None,
        "multiValueHeaders": None,
        "queryStringParameters": None,
        "multiValueQueryStringParameters": None,
        "pathParameters": {"media-id": "cba123"},
        # "pathParameters": None,
        "stageVariables": None,
        "requestContext": {
            "resourceId": "1c5yp2",
            "resourcePath": "/media/{media-id}/presigned-url",
            "httpMethod": "POST",
            "extendedRequestId": "fWRzHEQ3iYcFSfg=",
            "requestTime": "08/Oct/2024:20:30:50 +0000",
            "path": "/media/{media-id}/presigned-url",
            "accountId": "253320687396",
            "protocol": "HTTP/1.1",
            "stage": "test-invoke-stage",
            "domainPrefix": "testPrefix",
            "requestTimeEpoch": 1728419450066,
            "requestId": "7f04cb34-b2a3-498a-bf39-6478fe511e04",
            "identity": {
                "cognitoIdentityPoolId": None,
                "cognitoIdentityId": None,
                "apiKey": "test-invoke-api-key",
                "principalOrgId": None,
                "cognitoAuthenticationType": None,
                "userArn": "arn:aws:iam::253320687396:user/jchoi950",
                "apiKeyId": "test-invoke-api-key-id",
                "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                "accountId": "253320687396",
                "caller": "AIDATV6YW54SNCTMYTOGR",
                "sourceIp": "test-invoke-source-ip",
                "accessKey": "ASIATV6YW54SEDXTOH5D",
                "cognitoAuthenticationProvider": None,
                "user": "AIDATV6YW54SNCTMYTOGR",
            },
            "domainName": "testPrefix.testDomainName",
            "apiId": "upgyrrudrg",
        },
        "body": {"url": "https://choiflix.com/dev/test.mp4"},
        "isBase64Encoded": False,
    },
    LambdaContext(),
)

logger.debug(url)
