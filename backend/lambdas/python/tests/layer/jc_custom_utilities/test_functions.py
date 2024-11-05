import json
from jc_custom_utilities.functions import generate_api_response


class TestGenerateApiResponse:
    def test_response_structure(self):
        # Verifies that the function returns a dictionary with the required keys: statusCode, headers, and body
        status_code = 200
        body = {"message": "Success"}

        output = generate_api_response(status_code, body)

        assert "statusCode" in output
        assert "headers" in output
        assert "body" in output
        assert output["headers"]["Content-Type"] == "application/json"

    def test_status_code_404(self):
        # Tests that the statusCode in the response matches the input parameter
        input_codes = [200, 400, 404]

        valid_status_codes = {
            200: {"message": "Success"},
            400: {"message": "Bad Request"},
            404: {"message": "Not Found"},
        }

        for status_code in input_codes:
            body = valid_status_codes[status_code]
            output = generate_api_response(status_code, body)

            assert output["statusCode"] == status_code
            assert json.loads(output["body"]) == valid_status_codes[status_code]

    def test_body_serialization(self):
        # Validates that the body is properly serialized into JSON format and can be deserialized back to the original dictionary
        status_code = 200
        body = {"key": "value"}

        output = generate_api_response(status_code, body)

        output_body = json.loads(output["body"])

        assert output_body == body
