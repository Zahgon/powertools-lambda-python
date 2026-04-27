from __future__ import annotations

import base64
import inspect
import warnings
from typing import TYPE_CHECKING, Any, Callable
from urllib.parse import parse_qs

from aws_lambda_powertools.event_handler.api_gateway import (
    ApiGatewayResolver,
    BaseRouter,
    ProxyEventType,
    Response,
    Route,
)
from aws_lambda_powertools.event_handler.middlewares.async_utils import wrap_middleware_async
from aws_lambda_powertools.shared.headers_serializer import BaseHeadersSerializer
from aws_lambda_powertools.utilities.data_classes.common import BaseProxyEvent

if TYPE_CHECKING:
    from aws_lambda_powertools.shared.cookies import Cookie


class HttpHeadersSerializer(BaseHeadersSerializer):
    """Headers serializer for native HTTP responses."""

    def serialize(self, headers: dict[str, str | list[str]], cookies: list[Cookie]) -> dict[str, Any]:
        """Serialize headers for HTTP response format."""
        combined_headers: dict[str, str] = {}
        for key, values in headers.items():
            if values is None:  # pragma: no cover
                continue
            if isinstance(values, str):
                combined_headers[key] = values
            else:
                combined_headers[key] = ", ".join(values)

        # Add cookies as Set-Cookie headers
        cookie_headers = [str(cookie) for cookie in cookies] if cookies else []

        return {"headers": combined_headers, "cookies": cookie_headers}


class HttpProxyEvent(BaseProxyEvent):
    """
    A proxy event that wraps native HTTP request data.

    This allows the same route handlers to work with both Lambda and native HTTP servers.
    """

    def __init__(
        self,
        method: str,
        path: str,
        headers: dict[str, str] | None = None,
        body: str | bytes | None = None,
        query_string: str | None = None,
        path_parameters: dict[str, str] | None = None,
        request_context: dict[str, Any] | None = None,
    ):
        # Parse query string
        query_params: dict[str, str] = {}
        multi_query_params: dict[str, list[str]] = {}

        if query_string:
            parsed = parse_qs(query_string, keep_blank_values=True)
            multi_query_params = parsed
            query_params = {k: v[-1] for k, v in parsed.items()}

        # Normalize body to string
        body_str = None
        if body is not None:
            body_str = body.decode("utf-8") if isinstance(body, bytes) else body

        # Build the internal dict structure that BaseProxyEvent expects
        data = {
            "httpMethod": method.upper(),
            "path": path,
            "headers": headers or {},
            "body": body_str,
            "isBase64Encoded": False,
            "queryStringParameters": query_params,
            "multiValueQueryStringParameters": multi_query_params,
            "pathParameters": path_parameters or {},
            "requestContext": request_context
            or {
                "stage": "local",
                "requestId": "local-request-id",
                "http": {"method": method.upper(), "path": path},
            },
        }

        super().__init__(data)

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> HttpProxyEvent:
        """Create HttpProxyEvent directly from a dict (used internally)."""
        instance = object.__new__(cls)
        BaseProxyEvent.__init__(instance, data)
        return instance

    @classmethod
    def from_asgi(cls, scope: dict[str, Any], body: bytes | None = None) -> HttpProxyEvent:
        """
        Create an HttpProxyEvent from an ASGI scope dict.

        Parameters
        ----------
        scope : dict
            ASGI scope dictionary
        body : bytes, optional
            Request body

        Returns
        -------
        HttpProxyEvent
            Event object compatible with Powertools resolvers
        """
        pass

    def header_serializer(self) -> BaseHeadersSerializer:
        """Return the HTTP headers serializer."""
        return HttpHeadersSerializer()

    @property
    def resolved_query_string_parameters(self) -> dict[str, list[str]]:
        """Return query parameters in the format expected by OpenAPI validation."""
        pass

    @property
    def resolved_headers_field(self) -> dict[str, str]:
        """Return headers in the format expected by OpenAPI validation."""
        pass


class MockLambdaContext:
    """Minimal Lambda context for HTTP adapter."""

    function_name = "http-resolver"
    memory_limit_in_mb = 128
    invoked_function_arn = "arn:aws:lambda:local:000000000000:function:http-resolver"
    aws_request_id = "local-request-id"
    log_group_name = "/aws/lambda/http-resolver"
    log_stream_name = "local"

    def get_remaining_time_in_millis(self) -> int:  # pragma: no cover
        return 300000  # 5 minutes


class HttpResolverLocal(ApiGatewayResolver):
    """
    ASGI-compatible HTTP resolver for local development and testing.

    This resolver is designed specifically for local development workflows.
    It allows you to run your Powertools application locally with any ASGI server
    (uvicorn, hypercorn, daphne, etc.) while maintaining full compatibility with Lambda.

    The same code works in both environments - locally via ASGI and in Lambda via the handler.

    Supports both sync and async route handlers.

    WARNING
    -------
    This is intended for local development and testing only.
    The API may change in future releases. Do not use in production environments.

    Example
    -------
    ```python
    from aws_lambda_powertools.event_handler import HttpResolverLocal

    app = HttpResolverLocal()

    @app.get("/hello/<name>")
    async def hello(name: str):
        # Async handler - can use await
        return {"message": f"Hello, {name}!"}

    @app.get("/sync")
    def sync_handler():
        # Sync handlers also work
        return {"sync": True}

    # Run locally with uvicorn:
    # uvicorn app:app --reload

    # Deploy to Lambda (sync only):
    # handler = app
    ```
    """

    def __init__(
        self,
        cors: Any = None,
        debug: bool | None = None,
        serializer: Callable[[dict], str] | None = None,
        strip_prefixes: list[str | Any] | None = None,
        enable_validation: bool = False,
    ):
        warnings.warn(
            "HttpResolverLocal is intended for local development and testing only. "
            "The API may change in future releases. Do not use in production environments.",
            stacklevel=2,
        )
        super().__init__(
            proxy_type=ProxyEventType.APIGatewayProxyEvent,  # Use REST API format internally
            cors=cors,
            debug=debug,
            serializer=serializer,
            strip_prefixes=strip_prefixes,
            enable_validation=enable_validation,
        )
        self._is_async_mode = False

    def _to_proxy_event(self, event: dict) -> BaseProxyEvent:
        """Convert event dict to HttpProxyEvent."""
        # Create HttpProxyEvent directly from the dict data
        # The dict already has queryStringParameters and multiValueQueryStringParameters
        return HttpProxyEvent._from_dict(event)

    def _get_base_path(self) -> str:
        """Return the base path for HTTP resolver (no stage prefix)."""
        return ""

    async def _resolve_async(self) -> dict:  # type: ignore[override]
        """Async version of resolve that supports async handlers."""
        pass

    async def _call_route_async(self, route: Route, route_arguments: dict[str, str]) -> dict:  # type: ignore[override]
        """Call route handler, supporting both sync and async handlers."""
        pass

    async def _run_middleware_chain_async(self, route: Route) -> Response:
        """Run the middleware chain, awaiting async handlers."""
        pass

    async def _handle_not_found_async(self, method: str = "", path: str = "") -> dict:  # type: ignore[override]
        """Handle 404 responses, using custom not_found handler if registered."""
        pass

    async def asgi_handler(self, scope: dict, receive: Callable, send: Callable) -> None:
        """
        ASGI interface - allows running with uvicorn/hypercorn/etc.

        Parameters
        ----------
        scope : dict
            ASGI connection scope
        receive : Callable
            ASGI receive function
        send : Callable
            ASGI send function
        """
        pass

    async def __call__(  # type: ignore[override]
        self,
        scope: dict,
        receive: Callable,
        send: Callable,
    ) -> None:
        """ASGI interface - allows running with uvicorn/hypercorn/etc."""
        await self.asgi_handler(scope, receive, send)

    async def _send_response(self, send: Callable, response: dict) -> None:
        """Send the response via ASGI."""
        pass
