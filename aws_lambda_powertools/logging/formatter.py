from __future__ import annotations

import inspect
import json
import logging
import os
import time
import traceback
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
from functools import partial
from typing import TYPE_CHECKING, Any

from aws_lambda_powertools.shared import constants
from aws_lambda_powertools.shared.functions import powertools_dev_is_set

if TYPE_CHECKING:
    from collections.abc import Callable, Generator, Iterable

    from aws_lambda_powertools.logging.types import LogRecord, LogStackTrace

RESERVED_LOG_ATTRS = (
    "name",
    "msg",
    "args",
    "level",
    "levelname",
    "levelno",
    "pathname",
    "filename",
    "module",
    "exc_info",
    "exc_text",
    "stack_info",
    "lineno",
    "funcName",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process",
    "asctime",
    "location",
    "timestamp",
)


class BasePowertoolsFormatter(logging.Formatter, metaclass=ABCMeta):
    @abstractmethod
    def append_keys(self, **additional_keys) -> None:
        raise NotImplementedError()

    def get_current_keys(self) -> dict[str, Any]:
        pass

    def remove_keys(self, keys: Iterable[str]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def clear_state(self) -> None:
        """Removes any previously added logging keys"""
        raise NotImplementedError()

    @contextmanager
    def append_context_keys(self, **additional_keys: Any) -> Generator[None, None, None]:
        pass

    # These specific thread-safe methods are necessary to manage shared context in concurrent environments.
    # They prevent race conditions and ensure data consistency across multiple threads and logger.
    def thread_safe_append_keys(self, **additional_keys) -> None:
        raise NotImplementedError()

    def thread_safe_get_current_keys(self) -> dict[str, Any]:
        pass

    def thread_safe_remove_keys(self, keys: Iterable[str]) -> None:
        raise NotImplementedError()

    def thread_safe_clear_keys(self) -> None:
        """Removes any previously added logging keys in a specific thread"""
        raise NotImplementedError()


class LambdaPowertoolsFormatter(BasePowertoolsFormatter):
    """Powertools for AWS Lambda (Python) Logging formatter.

    Formats the log message as a JSON encoded string. If the message is a
    dict it will be used directly.
    """

    default_time_format = "%Y-%m-%d %H:%M:%S,%F%z"  # '2021-04-17 18:19:57,656+0200'
    custom_ms_time_directive = "%F"
    RFC3339_ISO8601_FORMAT = "%Y-%m-%dT%H:%M:%S.%F%z"  # '2022-10-27T16:27:43.738+02:00'

    def __init__(
        self,
        json_serializer: Callable[[LogRecord], str] | None = None,
        json_deserializer: Callable[[dict | str | bool | int | float], str] | None = None,
        json_default: Callable[[Any], Any] | None = None,
        datefmt: str | None = None,
        use_datetime_directive: bool = False,
        log_record_order: list[str] | None = None,
        utc: bool = False,
        use_rfc3339: bool = False,
        serialize_stacktrace: bool = True,
        **kwargs,
    ) -> None:
        """Return a LambdaPowertoolsFormatter instance.

        The `log_record_order` kwarg is used to specify the order of the keys used in
        the structured json logs. By default the order is: "level", "location", "message", "timestamp",
        "service".

        Other kwargs are used to specify log field format strings.

        Parameters
        ----------
        json_serializer : Callable, optional
            function to serialize `obj` to a JSON formatted `str`, by default json.dumps
        json_deserializer : Callable, optional
            function to deserialize `str`, `bytes`, bytearray` containing a JSON document to a Python `obj`,
            by default json.loads
        json_default : Callable, optional
            function to coerce unserializable values, by default str

            Only used when no custom JSON encoder is set

        datefmt : str, optional
            String directives (strftime) to format log timestamp.

            See https://docs.python.org/3/library/time.html#time.strftime or
        use_datetime_directive: str, optional
            Interpret `datefmt` as a format string for `datetime.datetime.strftime`, rather than
            `time.strftime` - Only useful when used alongside `datefmt`.

            See https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior . This
            also supports a custom %F directive for milliseconds.
        utc : bool, optional
            set logging timestamp to UTC, by default False to continue to use local time as per stdlib
        use_rfc3339: bool, optional
            Whether to use a popular dateformat that complies with both RFC3339 and ISO8601.
            e.g., 2022-10-27T16:27:43.738+02:00.
        log_record_order : list, optional
            set order of log keys when logging, by default ["level", "location", "message", "timestamp"]
        kwargs
            Key-value to be included in log messages

        """

        self.json_deserializer = json_deserializer or json.loads
        self.json_default = json_default or str
        self.json_indent = (
            constants.PRETTY_INDENT if powertools_dev_is_set() else constants.COMPACT_INDENT
        )  # indented json serialization when in AWS SAM Local
        self.json_serializer = json_serializer or partial(
            json.dumps,
            default=self.json_default,
            separators=(",", ":"),
            indent=self.json_indent,
            ensure_ascii=False,  # see #3474
        )

        self.datefmt = datefmt
        self.use_datetime_directive = use_datetime_directive

        self.utc = utc
        self.log_record_order = log_record_order or ["level", "location", "message", "timestamp"]
        self.log_format = dict.fromkeys(self.log_record_order)  # Set the insertion order for the log messages
        self.update_formatter = self.append_keys  # alias to old method
        self.use_rfc3339_iso8601 = use_rfc3339

        if self.utc:
            self.converter = time.gmtime
        else:
            self.converter = time.localtime

        self.keys_combined = {**self._build_default_keys(), **kwargs}
        self.log_format.update(**self.keys_combined)

        self.serialize_stacktrace = serialize_stacktrace

        super().__init__(datefmt=self.datefmt)

    def serialize(self, log: LogRecord) -> str:
        """Serialize structured log dict to JSON str"""
        return self.json_serializer(log)

    def format(self, record: logging.LogRecord) -> str:  # noqa: A003
        """Format logging record as structured JSON str"""
        pass

    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        # As of Py3.7, we can infer milliseconds directly from any datetime
        # saving processing time as we can shortcircuit early
        # Maintenance: In V3, we (and Java) should move to this format by default
        # since we've provided enough time for those migrating from std logging
        pass

    def append_keys(self, **additional_keys) -> None:
        self.log_format.update(additional_keys)

    def get_current_keys(self) -> dict[str, Any]:
        pass

    def remove_keys(self, keys: Iterable[str]) -> None:
        pass

    def clear_state(self) -> None:
        self.log_format = dict.fromkeys(self.log_record_order)
        self.log_format.update(**self.keys_combined)

    @contextmanager
    def append_context_keys(self, **additional_keys: Any) -> Generator[None, None, None]:
        """
        Context manager to temporarily add logging keys.

        Parameters
        -----------
        **additional_keys: Any
            Key-value pairs to include in the log context during the lifespan of the context manager.

        Warning
        -------
        All keys added within this context are removed when exiting, even if they existed before.
        If a key with the same name already exists, the original value will be lost after the context exits.
        To persist keys across multiple log messages, use `append_keys()` instead.

        Example
        --------
            logger = Logger(service="example_service")
            with logger.append_context_keys(user_id="123", operation="process"):
                logger.info("Log with context")
            logger.info("Log without context")
        """
        pass

    # These specific thread-safe methods are necessary to manage shared context in concurrent environments.
    # They prevent race conditions and ensure data consistency across multiple threads.
    def thread_safe_append_keys(self, **additional_keys) -> None:
        # Append additional key-value pairs to the context safely in a thread-safe manner.
        pass

    def thread_safe_get_current_keys(self) -> dict[str, Any]:
        # Retrieve the current context keys safely in a thread-safe manner.
        pass

    def thread_safe_remove_keys(self, keys: Iterable[str]) -> None:
        # Remove specified keys from the context safely in a thread-safe manner.
        pass

    def thread_safe_clear_keys(self) -> None:
        # Clear all keys from the context safely in a thread-safe manner.
        clear_context_keys()

    @staticmethod
    def _build_default_keys() -> dict[str, str]:
        return {
            "level": "%(levelname)s",
            "location": "%(funcName)s:%(lineno)d",
            "timestamp": "%(asctime)s",
        }

    def _get_latest_trace_id(self) -> str | None:
        pass

    def _extract_log_message(self, log_record: logging.LogRecord) -> dict[str, Any] | str | bool | Iterable:
        """Extract message from log record and attempt to JSON decode it if str

        Parameters
        ----------
        log_record : logging.LogRecord
            Log record to extract message from

        Returns
        -------
        message: dict[str, Any] | str | bool | Iterable
            Extracted message
        """
        pass

    def _serialize_stacktrace(self, log_record: logging.LogRecord) -> LogStackTrace | None:
        # Check if the first element of exc_info has the __name__ attribute,
        # which indicates it is likely an exception class or object.
        # See: https://github.com/aws-powertools/powertools-lambda-python/issues/6358
        pass

    def _extract_log_exception(self, log_record: logging.LogRecord) -> tuple[str, str, list] | tuple[None, None, None]:
        """Format traceback information, if available

        Parameters
        ----------
        log_record : logging.LogRecord
            Log record to extract message from

        Returns
        -------
        log_record: tuple[str, str] | tuple[None, None]
            Log record with constant traceback info and exception name
        """
        pass

    def _extract_log_keys(self, log_record: logging.LogRecord) -> dict[str, Any]:
        """Extract and parse custom and reserved log keys

        Parameters
        ----------
        log_record : logging.LogRecord
            Log record to extract keys from

        Returns
        -------
        formatted_log: dict[str, Any]
            Structured log as dictionary
        """
        pass

    @staticmethod
    def _strip_none_records(records: dict[str, Any]) -> dict[str, Any]:
        """Remove any key with None as value"""
        pass


JsonFormatter = LambdaPowertoolsFormatter  # alias to previous formatter


# Fetch current and future parameters from PowertoolsFormatter that should be reserved
RESERVED_FORMATTER_CUSTOM_KEYS: list[str] = inspect.getfullargspec(LambdaPowertoolsFormatter).args[1:]

# ContextVar for thread local keys
default_contextvar: dict[str, Any] = {}

THREAD_LOCAL_KEYS: ContextVar[dict[str, Any]] = ContextVar("THREAD_LOCAL_KEYS", default=default_contextvar)


def _get_context() -> ContextVar[dict[str, Any]]:
    return THREAD_LOCAL_KEYS


def clear_context_keys() -> None:
    _get_context().set({})


def set_context_keys(**kwargs: dict[str, Any]) -> None:
    pass


def remove_context_keys(keys: Iterable[str]) -> None:
    pass
