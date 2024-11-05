import os
from http import HTTPStatus
from dotenv import load_dotenv
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

# instantiate ddb resource table globally
metadata_table = DynamoDBResourceTable(os.getenv("METADATA_DDB_TABLE_NAME"))


def handler(event: APIGatewayProxyEvent, context: LambdaContext):
    logger.debug(event)

    http_method: HTTPMethod = event.get("httpMethod")
    path: str = event.get("path")
    path_parameters: dict | None = event.get("pathParameters", {})

    # Check for GET /medias
    if path == "/medias" and http_method == "GET":
        return get_medias()

    # Check for GET /medias/{id}
    if path.startswith("/medias/") and http_method == "GET" and path_parameters:
        return get_media_by_id(path_parameters.get("media-id"))

    return generate_api_response(
        status_code=HTTPStatus.BAD_REQUEST,
        body={"message": f"Bad request - path: '{path}'"},
    )


def get_medias():
    global metadata_table

    try:
        logger.info("scanning ddb for items...")
        response: dict = metadata_table.scan()

        logger.debug(response)

        status_code = HTTPStatus.OK
        body = response

    except ValueError as e:
        status_code = HTTPStatus.BAD_REQUEST
        body = {"message": f"{e}"}

    except Exception as e:
        status_code = HTTPStatus.NOT_FOUND
        body = {"message": f"{e}"}

    finally:
        # format/generate api response and return
        return generate_api_response(status_code=status_code, body=body)


def get_media_by_id(media_id: str):
    global metadata_table
    try:
        logger.info("retrieving metadata from ddb...")
        response: dict = metadata_table.get_item(Key={"id": media_id})
        logger.debug(response)

        if not response.get("Item"):
            logger.info("metadata not found")
            status_code = HTTPStatus.NOT_FOUND
            body = {"message": "Media not found."}
        else:
            logger.info("metadata found")
            status_code = HTTPStatus.OK
            body = response

    except ValueError as e:
        status_code = HTTPStatus.BAD_REQUEST
        body = {"message": f"{e}"}

    except Exception as e:
        status_code = HTTPStatus.NOT_FOUND
        body = {"message": f"{e}"}

    finally:
        # format/generate api response and return
        return generate_api_response(status_code=status_code, body=body)


api_res = handler(
    {
        "resource": "/medias",
        "path": "/medias/abc123",
        "httpMethod": "GET",
        "headers": None,
        "multiValueHeaders": None,
        "queryStringParameters": None,
        "multiValueQueryStringParameters": None,
        # "pathParameters": None,
        "pathParameters": {"media-id": "abc123"},
        "stageVariables": None,
        "requestContext": {
            "resourceId": "zf7ub0",
            "resourcePath": "/media",
            "httpMethod": "GET",
            "extendedRequestId": "fWEOAFdziYcF_7A=",
            "requestTime": "08/Oct/2024:18:58:07 +0000",
            "path": "/media/{media_id}",
            "accountId": "253320687396",
            "protocol": "HTTP/1.1",
            "stage": "test-invoke-stage",
            "domainPrefix": "testPrefix",
            "requestTimeEpoch": 1728413887748,
            "requestId": "e8535d80-c9fd-43ae-94bd-f8bac240def2",
            "identity": {},
            "domainName": "testPrefix.testDomainName",
            "apiId": "upgyrrudrg",
        },
        "body": None,
        "isBase64Encoded": False,
    },
    LambdaContext(),
)

logger.info(api_res)
