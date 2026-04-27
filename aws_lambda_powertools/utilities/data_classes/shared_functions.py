from __future__ import annotations

import base64
import warnings
from typing import Any, overload

from typing_extensions import deprecated

from aws_lambda_powertools.warnings import PowertoolsDeprecationWarning


def base64_decode(value: str) -> str:
    """
    Decodes a Base64-encoded string and returns the decoded value.

    Parameters
    ----------
    value: str
        The Base64-encoded string to decode.

    Returns
    -------
    str
        The decoded string value.
    """
    pass


@overload
def get_header_value(
    headers: dict[str, Any],
    name: str,
    default_value: str,
    case_sensitive: bool = False,
) -> str: ...


@overload
def get_header_value(
    headers: dict[str, Any],
    name: str,
    default_value: str | None = None,
    case_sensitive: bool = False,
) -> str | None: ...


@deprecated(
    "`get_header_value` function is deprecated; Access headers directly using event.headers.get('HeaderName')",
    category=None,
)
def get_header_value(
    headers: dict[str, Any],
    name: str,
    default_value: str | None = None,
    case_sensitive: bool = False,
) -> str | None:
    """
    Get the value of a header by its name.
    Parameters
    ----------
    headers: Dict[str, str]
        The dictionary of headers.
    name: str
        The name of the header to retrieve.
    default_value: str, optional
        The default value to return if the header is not found. Default is None.
    case_sensitive: bool, optional
        Indicates whether the header name should be case-sensitive. Default is False.
    Returns
    -------
    str, optional
        The value of the header if found, otherwise the default value or None.
    """
    pass


@overload
def get_query_string_value(
    query_string_parameters: dict[str, str] | None,
    name: str,
    default_value: str,
) -> str: ...


@overload
def get_query_string_value(
    query_string_parameters: dict[str, str] | None,
    name: str,
    default_value: str | None = None,
) -> str | None: ...


def get_query_string_value(
    query_string_parameters: dict[str, str] | None,
    name: str,
    default_value: str | None = None,
) -> str | None:
    """
    Retrieves the value of a query string parameter specified by the given name.
    Parameters
    ----------
    name: str
        The name of the query string parameter to retrieve.
    default_value: str, optional
        The default value to return if the parameter is not found. Defaults to None.
    Returns
    -------
    str. optional
        The value of the query string parameter if found, or the default value if not found.
    """
    params = query_string_parameters
    return default_value if params is None else params.get(name, default_value)


def get_multi_value_query_string_values(
    multi_value_query_string_parameters: dict[str, list[str]] | None,
    name: str,
    default_values: list[str] | None = None,
) -> list[str]:
    """
    Retrieves the values of a multi-value string parameters specified by the given name.
    Parameters
    ----------
    name: str
        The name of the query string parameter to retrieve.
    default_value: list[str], optional
        The default value to return if the parameter is not found. Defaults to None.
    Returns
    -------
    List[str]. optional
        The values of the query string parameter if found, or the default values if not found.
    """
    pass
