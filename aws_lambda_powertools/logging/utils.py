from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from aws_lambda_powertools.logging.buffer.handler import BufferingHandler

if TYPE_CHECKING:
    from collections.abc import Callable

    from aws_lambda_powertools.logging.logger import Logger

PACKAGE_LOGGER = "aws_lambda_powertools"
LOGGER = logging.getLogger(__name__)


def copy_config_to_registered_loggers(
    source_logger: Logger,
    log_level: int | str | None = None,
    ignore_log_level=False,
    include_buffering=False,
    exclude: set[str] | None = None,
    include: set[str] | None = None,
) -> None:
    """Copies source Logger level and handler to all registered loggers for consistent formatting.

    Parameters
    ----------
    ignore_log_level
    source_logger : Logger
        Powertools for AWS Lambda (Python) Logger to copy configuration from
    log_level : int | str, optional
        Logging level to set to registered loggers, by default uses source_logger logging level
    ignore_log_level: bool
        Whether to not touch log levels for discovered loggers. log_level param is disregarded when this is set.
    include_buffering: bool
        Whether to buffer logs from external libraries and report to powertools logger
    include : set[str] | None, optional
        List of logger names to include, by default all registered loggers are included
    exclude : set[str] | None, optional
        List of logger names to exclude, by default None
    """
    pass


def _include_registered_loggers_filter(loggers: set[str]):
    pass


def _exclude_registered_loggers_filter(loggers: set[str]) -> list[logging.Logger]:
    pass


def _find_registered_loggers(
    loggers: set[str],
    filter_func: Callable[[set[str]], list[logging.Logger]],
) -> list[logging.Logger]:
    """Filter root loggers based on provided parameters."""
    pass


def _configure_logger(
    source_logger: Logger,
    logger: logging.Logger,
    level: int | str,
    ignore_log_level: bool = False,
    include_buffering: bool = False,
) -> None:
    # customers may not want to copy the same log level from Logger to discovered loggers
    pass
