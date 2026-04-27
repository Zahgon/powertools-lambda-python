class LambdaCognitoIdentity:
    """Information about the Amazon Cognito identity that authorized the request."""

    _cognito_identity_id: str
    _cognito_identity_pool_id: str

    @property
    def cognito_identity_id(self) -> str:
        """The authenticated Amazon Cognito identity."""
        pass

    @property
    def cognito_identity_pool_id(self) -> str:
        """The Amazon Cognito identity pool that authorized the invocation."""
        pass
