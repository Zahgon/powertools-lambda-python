from __future__ import annotations

from functools import cached_property
from typing import Any

from aws_lambda_powertools.shared.headers_serializer import (
    BaseHeadersSerializer,
    HttpApiHeadersSerializer,
    MultiValueHeadersSerializer,
)
from aws_lambda_powertools.utilities.data_classes.common import (
    BaseProxyEvent,
    BaseRequestContext,
    BaseRequestContextV2,
    CaseInsensitiveDict,
    DictWrapper,
)


class APIGatewayEventAuthorizer(DictWrapper):
    @property
    def claims(self) -> dict[str, Any]:
        pass

    @property
    def scopes(self) -> list[str]:
        pass

    @property
    def principal_id(self) -> str:
        """The principal user identification associated with the token sent by the client and returned from an
        API Gateway Lambda authorizer (formerly known as a custom authorizer)"""
        pass

    @property
    def integration_latency(self) -> int | None:
        """The authorizer latency in ms."""
        pass

    def get_context(self) -> dict[str, Any]:
        """Retrieve the authorization context details injected by a Lambda Authorizer.

        Example
        --------

        ```python
        ctx: dict = request_context.authorizer.get_context()

        tenant_id = ctx.get("tenant_id")
        ```

        Returns:
        --------
        dict[str, Any]
            A dictionary containing Lambda authorization context details.
        """
        pass


class APIGatewayEventRequestContext(BaseRequestContext):
    @property
    def connected_at(self) -> int | None:
        """The Epoch-formatted connection time. (WebSocket API)"""
        pass

    @property
    def connection_id(self) -> str | None:
        """A unique ID for the connection that can be used to make a callback to the client. (WebSocket API)"""
        pass

    @property
    def event_type(self) -> str | None:
        """The event type: `CONNECT`, `MESSAGE`, or `DISCONNECT`. (WebSocket API)"""
        pass

    @property
    def message_direction(self) -> str | None:
        """Message direction (WebSocket API)"""
        pass

    @property
    def message_id(self) -> str | None:
        """A unique server-side ID for a message. Available only when the `eventType` is `MESSAGE`."""
        pass

    @property
    def operation_name(self) -> str | None:
        """The name of the operation being performed"""
        pass

    @property
    def route_key(self) -> str | None:
        """The selected route key."""
        pass

    @property
    def authorizer(self) -> APIGatewayEventAuthorizer:
        pass


class APIGatewayProxyEvent(BaseProxyEvent):
    """AWS Lambda proxy V1

    Documentation:
    --------------
    - https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    """

    @property
    def version(self) -> str:
        return self["version"]

    @property
    def resource(self) -> str:
        return self["resource"]

    @property
    def multi_value_headers(self) -> dict[str, list[str]]:
        pass

    @property
    def resolved_query_string_parameters(self) -> dict[str, list[str]]:
        pass

    @property
    def resolved_headers_field(self) -> dict[str, Any]:
        pass

    @property
    def request_context(self) -> APIGatewayEventRequestContext:
        pass

    @property
    def path_parameters(self) -> dict[str, str]:
        pass

    @property
    def stage_variables(self) -> dict[str, str]:
        pass

    def header_serializer(self) -> BaseHeadersSerializer:
        return MultiValueHeadersSerializer()


class RequestContextV2AuthorizerIam(DictWrapper):
    @property
    def access_key(self) -> str:
        """The IAM user access key associated with the request."""
        pass

    @property
    def account_id(self) -> str:
        """The AWS account ID associated with the request."""
        pass

    @property
    def caller_id(self) -> str:
        """The principal identifier of the caller making the request."""
        pass

    def _cognito_identity(self) -> dict:
        pass

    @property
    def cognito_amr(self) -> list[str]:
        """This represents how the user was authenticated.
        AMR stands for  Authentication Methods References as per the openid spec"""
        pass

    @property
    def cognito_identity_id(self) -> str:
        """The Amazon Cognito identity ID of the caller making the request.
        Available only if the request was signed with Amazon Cognito credentials."""
        pass

    @property
    def cognito_identity_pool_id(self) -> str:
        """The Amazon Cognito identity pool ID of the caller making the request.
        Available only if the request was signed with Amazon Cognito credentials."""
        pass

    @property
    def principal_org_id(self) -> str:
        """The AWS organization ID."""
        pass

    @property
    def user_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the effective user identified after authentication."""
        pass

    @property
    def user_id(self) -> str:
        """The IAM user ID of the effective user identified after authentication."""
        pass


class RequestContextV2Authorizer(DictWrapper):
    @property
    def jwt_claim(self) -> dict[str, Any]:
        pass

    @property
    def jwt_scopes(self) -> list[str]:
        pass

    @property
    def get_lambda(self) -> dict[str, Any]:
        """Lambda authorization context details"""
        pass

    def get_context(self) -> dict[str, Any]:
        """Retrieve the authorization context details injected by a Lambda Authorizer.

        Example
        --------

        ```python
        ctx: dict = request_context.authorizer.get_context()

        tenant_id = ctx.get("tenant_id")
        ```

        Returns:
        --------
        dict[str, Any]
            A dictionary containing Lambda authorization context details.
        """
        pass

    @property
    def iam(self) -> RequestContextV2AuthorizerIam:
        """IAM authorization details used for making the request."""
        pass


class RequestContextV2(BaseRequestContextV2):
    @property
    def authorizer(self) -> RequestContextV2Authorizer:
        pass


class APIGatewayProxyEventV2(BaseProxyEvent):
    """AWS Lambda proxy V2 event

    Notes:
    -----
    Format 2.0 doesn't have multiValueHeaders or multiValueQueryStringParameters fields. Duplicate headers
    are combined with commas and included in the headers field. Duplicate query strings are combined with
    commas and included in the queryStringParameters field.

    Format 2.0 includes a new cookies field. All cookie headers in the request are combined with commas and
    added to the cookies field. In the response to the client, each cookie becomes a set-cookie header.

    Documentation:
    --------------
    - https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    """

    @property
    def version(self) -> str:
        return self["version"]

    @property
    def route_key(self) -> str:
        pass

    @property
    def raw_path(self) -> str:
        pass

    @property
    def raw_query_string(self) -> str:
        pass

    @property
    def cookies(self) -> list[str]:
        pass

    @property
    def resolved_cookies_field(self) -> dict[str, str]:
        """
        Parse cookies from the dedicated ``cookies`` field in API Gateway HTTP API v2 format.

        The ``cookies`` field contains a list of strings like ``["session=abc", "theme=dark"]``.
        """
        pass

    @property
    def request_context(self) -> RequestContextV2:
        pass

    @property
    def path_parameters(self) -> dict[str, str]:
        pass

    @property
    def stage_variables(self) -> dict[str, str]:
        pass

    @property
    def path(self) -> str:
        pass

    @property
    def http_method(self) -> str:
        """The HTTP method used. Valid values include: DELETE, GET, HEAD, OPTIONS, PATCH, POST, and PUT."""
        pass

    def header_serializer(self):
        return HttpApiHeadersSerializer()

    @cached_property
    def resolved_headers_field(self) -> dict[str, Any]:
        pass
