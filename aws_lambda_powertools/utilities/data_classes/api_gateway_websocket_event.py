from __future__ import annotations

import base64
from functools import cached_property
from typing import Any

from aws_lambda_powertools.utilities.data_classes.common import (
    CaseInsensitiveDict,
    DictWrapper,
)


class APIGatewayWebSocketEventIdentity(DictWrapper):
    @property
    def source_ip(self) -> str:
        pass

    @property
    def user_agent(self) -> str | None:
        pass


class APIGatewayWebSocketEventRequestContext(DictWrapper):
    @property
    def route_key(self) -> str:
        pass

    @property
    def disconnect_status_code(self) -> int | None:
        pass

    @property
    def message_id(self) -> str | None:
        pass

    @property
    def event_type(self) -> str:
        pass

    @property
    def extended_request_id(self) -> str:
        pass

    @property
    def request_time(self) -> str:
        pass

    @property
    def message_direction(self) -> str:
        pass

    @property
    def disconnect_reason(self) -> str | None:
        pass

    @property
    def stage(self) -> str:
        pass

    @property
    def connected_at(self) -> int:
        pass

    @property
    def request_time_epoch(self) -> int:
        pass

    @property
    def identity(self) -> APIGatewayWebSocketEventIdentity:
        pass

    @property
    def request_id(self) -> str:
        pass

    @property
    def domain_name(self) -> str:
        pass

    @property
    def connection_id(self) -> str:
        pass

    @property
    def api_id(self) -> str:
        pass


class APIGatewayWebSocketEvent(DictWrapper):
    """AWS proxy integration event for WebSocket API

    Documentation:
    --------------
    - https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-integration-requests.html
    """

    @property
    def is_base64_encoded(self) -> bool:
        pass

    @property
    def body(self) -> str | None:
        pass

    @cached_property
    def decoded_body(self) -> str | None:
        pass

    @cached_property
    def json_body(self) -> Any:
        pass

    @property
    def headers(self) -> dict[str, str]:
        pass

    @property
    def multi_value_headers(self) -> dict[str, list[str]]:
        pass

    @property
    def query_string_parameters(self) -> dict[str, str]:
        pass

    @property
    def multi_value_query_string_parameters(self) -> dict[str, list[str]]:
        pass

    @property
    def request_context(self) -> APIGatewayWebSocketEventRequestContext:
        pass
