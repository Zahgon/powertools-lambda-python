"""Standalone functions to serialize/deserialize common data structures"""

import base64
import json
from collections.abc import Callable
from typing import Any


def base64_encode(data: str) -> str:
    """Encode a string and returns Base64-encoded encoded value.

    Parameters
    ----------
    data: str
        The string to encode.

    Returns
    -------
    str
        The Base64-encoded encoded value.
    """
    pass


def base64_decode(data: str) -> str:
    """Decodes a Base64-encoded string and returns the decoded value.

    Parameters
    ----------
    data: str
        The Base64-encoded string to decode.

    Returns
    -------
    str
        The decoded string value.
    """
    pass


def base64_from_str(data: str) -> str:
    """Encode str as base64 string"""
    pass


def base64_from_json(data: Any, json_serializer: Callable[..., str] = json.dumps) -> str:
    """Encode JSON serializable data as base64 string

    Parameters
    ----------
    data: Any
        JSON serializable (dict, list, boolean, etc.)
    json_serializer: Callable
        function to serialize `obj` to a JSON formatted `str`, by default json.dumps

    Returns
    -------
    str:
        JSON string as base64 string
    """
    pass
