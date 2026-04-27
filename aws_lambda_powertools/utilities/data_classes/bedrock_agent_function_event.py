from __future__ import annotations

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper


class BedrockAgentInfo(DictWrapper):
    @property
    def name(self) -> str:
        pass

    @property
    def id(self) -> str:  # noqa: A003
        pass

    @property
    def alias(self) -> str:
        pass

    @property
    def version(self) -> str:
        return self["version"]


class BedrockAgentFunctionParameter(DictWrapper):
    @property
    def name(self) -> str:
        pass

    @property
    def type(self) -> str:  # noqa: A003
        pass

    @property
    def value(self) -> str:
        pass


class BedrockAgentFunctionEvent(DictWrapper):
    """
    Bedrock Agent Function input event

    Documentation:
    https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html
    """

    @property
    def message_version(self) -> str:
        pass

    @property
    def input_text(self) -> str:
        pass

    @property
    def session_id(self) -> str:
        pass

    @property
    def action_group(self) -> str:
        pass

    @property
    def function(self) -> str:
        return self["function"]

    @property
    def parameters(self) -> list[BedrockAgentFunctionParameter]:
        pass

    @property
    def agent(self) -> BedrockAgentInfo:
        pass

    @property
    def session_attributes(self) -> dict[str, str]:
        pass

    @property
    def prompt_session_attributes(self) -> dict[str, str]:
        pass
