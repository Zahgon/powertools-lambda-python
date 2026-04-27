"""Async middleware utilities for bridging sync and async middleware execution."""

from __future__ import annotations

import asyncio
import inspect
import logging
import threading
from typing import TYPE_CHECKING, Any

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from collections.abc import Callable

    from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver, BedrockResponse, Response


def wrap_middleware_async(middleware: Callable, next_handler: Callable) -> Callable:
    """Wrap a middleware to work in an async context.

    For async middlewares, delegates directly with ``await``.

    For sync middlewares, runs the middleware in a background thread and uses
    ``asyncio.Event`` / ``threading.Event`` to coordinate the ``next()`` call
    so the async handler can be awaited on the main event-loop while the sync
    middleware blocks its own thread waiting for the result.

    Parameters
    ----------
    middleware : Callable
        A sync or async middleware ``(app, next_middleware) -> Response``.
    next_handler : Callable
        The next (async) handler in the chain.

    Returns
    -------
    Callable
        An async callable ``(app) -> Response`` that executes *middleware*
        followed by *next_handler*.
    """
    pass


async def _run_sync_middleware_in_thread(
    middleware: Callable,
    next_handler: Callable,
    app: Any,
) -> Any:
    """Execute a **sync** middleware inside a daemon thread.

    The sync middleware calls ``sync_next(app)`` which:

    1. Signals the async side that the middleware is ready for the next handler.
    2. Blocks the thread until the async handler has produced a response.
    3. Returns the response so the middleware can do post-processing.

    Meanwhile the async side awaits *next_handler*, feeds the response back,
    and waits for the thread to finish.
    """
    pass


class AsyncMiddlewareFrame:
    """Async version of MiddlewareFrame for the async middleware chain.

    Each instance wraps a middleware (sync or async) and the next handler in the stack.
    When called, it auto-detects whether the current middleware is sync or async:

    - **Async middleware**: awaited directly with ``(app, next_middleware)``
    - **Sync middleware**: executed in a background thread so the event loop is never blocked

    Parameters
    ----------
    current_middleware : Callable
        The current middleware function to be called as a request is processed.
    next_middleware : Callable
        The next middleware in the middleware stack.
    """

    def __init__(
        self,
        current_middleware: Callable[..., Any],
        next_middleware: Callable[..., Any],
    ) -> None:
        self.current_middleware: Callable[..., Any] = current_middleware
        self.next_middleware: Callable[..., Any] = next_middleware
        self._next_middleware_name = next_middleware.__name__

    @property
    def __name__(self) -> str:  # noqa: A003
        return self.current_middleware.__name__

    def __str__(self) -> str:
        middleware_name = self.__name__
        return f"[{middleware_name}] next call chain is {middleware_name} -> {self._next_middleware_name}"

    async def __call__(self, app: ApiGatewayResolver) -> dict | tuple | Response:
        logger.debug("AsyncMiddlewareFrame: %s", self)
        app._push_processed_stack_frame(str(self))

        if inspect.iscoroutinefunction(self.current_middleware):
            return await self.current_middleware(app, self.next_middleware)

        loop = asyncio.get_running_loop()

        def sync_next(app: ApiGatewayResolver) -> Any:
            pass

        return await asyncio.to_thread(self.current_middleware, app, sync_next)


async def _registered_api_adapter_async(
    app: ApiGatewayResolver,
    next_middleware: Callable[..., Any],
) -> dict | tuple | Response | BedrockResponse:
    """
    Async version of _registered_api_adapter.

    Detects if the route handler is a coroutine and awaits it.
    _to_response() stays sync (CPU-bound — no async benefit).

    IMPORTANT: This is an internal building block only.
    Nothing calls it in the resolve chain yet. It will be used
    by resolve_async() (see issue #8137).

    Parameters
    ----------
    app: ApiGatewayResolver
        The API Gateway resolver
    next_middleware: Callable[..., Any]
        The function to handle the API

    Returns
    -------
    Response
        The API Response Object
    """
    pass
