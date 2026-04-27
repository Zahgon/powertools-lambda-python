from typing import Literal

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper


class SecretsManagerEvent(DictWrapper):
    @property
    def secret_id(self) -> str:
        """SecretId: The secret ARN or identifier"""
        pass

    @property
    def client_request_token(self) -> str:
        """ClientRequestToken: The ClientRequestToken associated with the secret version"""
        pass

    @property
    def version_id(self) -> str:
        """Alias to ClientRequestToken to get token associated to version"""
        pass

    @property
    def step(self) -> Literal["createSecret", "setSecret", "testSecret", "finishSecret"]:
        """Step: The rotation step (one of createSecret, setSecret, testSecret, or finishSecret)"""
        pass
