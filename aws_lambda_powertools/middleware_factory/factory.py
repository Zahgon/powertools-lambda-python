from __future__ import annotations

import functools
import inspect
import logging
import os
from typing import TYPE_CHECKING, Any

from aws_lambda_powertools.middleware_factory.exceptions import MiddlewareInvalidArgumentError
from aws_lambda_powertools.shared import constants
from aws_lambda_powertools.shared.functions import resolve_truthy_env_var_choice
from aws_lambda_powertools.tracing import Tracer

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from collections.abc import Callable


# Maintenance: we can't yet provide an accurate return type without ParamSpec etc. see #1066
def lambda_handler_decorator(decorator: Callable | None = None, trace_execution: bool | None = None) -> Callable:
    """Decorator factory for decorating Lambda handlers.

    You can use lambda_handler_decorator to create your own middlewares,
    where your function signature follows: `fn(handler, event, context)`

    Custom keyword arguments are also supported e.g. `fn(handler, event, context, option=value)`

    Middlewares created by this factory supports tracing to help you quickly troubleshoot
    any overhead that custom middlewares may cause - They will appear as custom subsegments.

    **Non-key value params are not supported** e.g. `fn(handler, event, context, option)`

    Environment variables
    ---------------------
    POWERTOOLS_TRACE_MIDDLEWARES : str
        uses `aws_lambda_powertools.tracing.Tracer`
        to create sub-segments per middleware (e.g. `"true", "True", "TRUE"`)

    Parameters
    ----------
    decorator: Callable
        Middleware to be wrapped by this factory
    trace_execution: bool
        Flag to explicitly enable trace execution for middlewares.\n
        `Env POWERTOOLS_TRACE_MIDDLEWARES="true"`

    Example
    -------
    **Create a middleware no params**

        from aws_lambda_powertools.middleware_factory import lambda_handler_decorator

        @lambda_handler_decorator
        def log_response(handler, event, context):
            any_code_to_execute_before_lambda_handler()
            response = handler(event, context)
            any_code_to_execute_after_lambda_handler()
            print(f"Lambda handler response: {response}")

        @log_response
        def lambda_handler(event, context):
            return True

    **Create a middleware with params**

        from aws_lambda_powertools.middleware_factory import lambda_handler_decorator

        @lambda_handler_decorator
        def obfuscate_sensitive_data(handler, event, context, fields=None):
            # Obfuscate email before calling Lambda handler
            if fields:
                for field in fields:
                    field = event.get(field, "")
                    event[field] = obfuscate_pii(field)

            response = handler(event, context)
            print(f"Lambda handler response: {response}")

        @obfuscate_sensitive_data(fields=["email"])
        def lambda_handler(event, context):
            return True

    **Trace execution of custom middleware**

        from aws_lambda_powertools import Tracer
        from aws_lambda_powertools.middleware_factory import lambda_handler_decorator

        tracer = Tracer(service="payment") # or via env var
        ...
        @lambda_handler_decorator(trace_execution=True)
        def log_response(handler, event, context):
            ...

        @tracer.capture_lambda_handler
        @log_response
        def lambda_handler(event, context):
            return True

    Limitations
    -----------
    * Async middlewares not supported
    * Classes, class methods middlewares not supported

    Raises
    ------
    MiddlewareInvalidArgumentError
        When middleware receives non keyword=arguments
    """
    pass
