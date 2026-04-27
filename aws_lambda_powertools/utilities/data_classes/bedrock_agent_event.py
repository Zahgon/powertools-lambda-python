from __future__ import annotations

from functools import cached_property
from typing import Any

from aws_lambda_powertools.utilities.data_classes.common import BaseProxyEvent, DictWrapper


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


class BedrockAgentProperty(DictWrapper):
    @property
    def name(self) -> str:
        pass

    @property
    def type(self) -> str:  # noqa: A003
        pass

    @property
    def value(self) -> str:
        pass


class BedrockAgentRequestMedia(DictWrapper):
    @property
    def properties(self) -> list[BedrockAgentProperty]:
        pass


class BedrockAgentRequestBody(DictWrapper):
    @property
    def content(self) -> dict[str, BedrockAgentRequestMedia]:
        pass


class BedrockAgentEvent(BaseProxyEvent):
    """
    Bedrock Agent input event

    See https://docs.aws.amazon.com/bedrock/latest/userguide/agents-create.html
    """

    # httpMethod is inherited from BaseProxyEvent class.

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
    def api_path(self) -> str:
        pass

    @property
    def parameters(self) -> list[BedrockAgentProperty]:
        pass

    @property
    def request_body(self) -> BedrockAgentRequestBody | None:
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

    # The following methods add compatibility with BaseProxyEvent
    @property
    def path(self) -> str:
        pass

    @cached_property
    def query_string_parameters(self) -> dict[str, str]:
        # In Bedrock Agent events, query string parameters are passed as undifferentiated parameters,
        # together with the other parameters. So we just return all parameters here.
        pass

    @property
    def resolved_query_string_parameters(self) -> dict[str, list[str]]:
        """
        Override the base implementation to prevent splitting parameter values by commas.

        For Bedrock Agent events, parameters are already properly structured and should not
        be split by commas as they might contain commas as part of their actual values
        (e.g., SQL queries).
        """
        pass

    @property
    def resolved_headers_field(self) -> dict[str, Any]:
        pass

    @cached_property
    def json_body(self) -> Any:
        # In Bedrock Agent events, body parameters are encoded differently
        # @see https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html#agents-lambda-input
        pass
