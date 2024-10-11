from enum import Enum
from typing import Literal


class HTTPMethod(str, Enum):
    """HTTP Methods
    * GET
    * POST
    * PUT
    * DELETE
    * PATCH
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
