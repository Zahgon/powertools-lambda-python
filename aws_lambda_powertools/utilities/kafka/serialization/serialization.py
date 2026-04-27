from __future__ import annotations

import sys
from dataclasses import is_dataclass
from types import UnionType  # Available in Python 3.10+
from typing import TYPE_CHECKING, Annotated, Any, Optional, Union, get_args, get_origin

from aws_lambda_powertools.utilities.kafka.serialization.custom_dict import CustomDictOutputSerializer
from aws_lambda_powertools.utilities.kafka.serialization.dataclass import DataclassOutputSerializer

if TYPE_CHECKING:
    from collections.abc import Callable

    from aws_lambda_powertools.utilities.kafka.serialization.types import T


def _get_output_serializer(output: type[T] | Callable | None = None) -> Any:
    """
    Returns the appropriate serializer for the given output class.
    Uses lazy imports to avoid unnecessary dependencies.
    """
    pass


def _is_pydantic_model(obj: Any) -> bool:
    pass


def serialize_to_output_type(
    data: object | dict[str, Any],
    output: type[T] | Callable | None = None,
) -> T | dict[str, Any]:
    """
    Helper function to directly serialize data to the specified output class
    """
    pass
