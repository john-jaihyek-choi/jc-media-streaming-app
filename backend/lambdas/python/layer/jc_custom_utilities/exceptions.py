class InvalidSignedUrlError(Exception):
    """Exception raised for errors in CloudFrontSignerHelper."""

    def __init__(self, message="The pre-signed url is invalid"):
        self.message = message
        super().__init__(self.message)
