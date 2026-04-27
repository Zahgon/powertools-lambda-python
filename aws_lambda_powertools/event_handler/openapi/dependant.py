from __future__ import annotations

import inspect
import re
from typing import TYPE_CHECKING, Any, ForwardRef, cast

from aws_lambda_powertools.event_handler.depends import DependencyParam, _get_depends_from_annotation
from aws_lambda_powertools.event_handler.openapi.compat import (
    ModelField,
    create_body_model,
    evaluate_forwardref,
    is_scalar_field,
)
from aws_lambda_powertools.event_handler.openapi.params import (
    Body,
    Dependant,
    File,
    Form,
    Param,
    ParamTypes,
    analyze_param,
    create_response_field,
    get_flat_dependant,
)
from aws_lambda_powertools.event_handler.openapi.types import OpenAPIResponse, OpenAPIResponseContentModel
from aws_lambda_powertools.event_handler.request import Request

if TYPE_CHECKING:
    from collections.abc import Callable

    from pydantic import BaseModel

"""
This turns the opaque function signature into typed, validated models.

It relies on Pydantic's typing and validation to achieve this in a declarative way.
This enables traits like autocompletion, validation, and declarative structure vs imperative parsing.

This code parses an OpenAPI operation handler function signature into Pydantic models. It uses inspect to get the
signature and regex to parse path parameters. Each parameter is analyzed to extract its type annotation and generate
a corresponding Pydantic field, which are added to a Dependant model. Return values are handled similarly.

This modeling allows for type checking, automatic parameter name/location/type extraction, and input validation -
turning the opaque signature into validated models. It relies on Pydantic's typing and validation for a declarative
approach over imperative parsing, enabling autocompletion, validation and structure.
"""


def add_param_to_fields(
    *,
    field: ModelField,
    dependant: Dependant,
) -> None:
    """
    Adds a parameter to the list of parameters in the dependant model.

    Parameters
    ----------
    field: ModelField
        The field to add
    dependant: Dependant
        The dependant model to add the field to

    """
    pass


def get_typed_annotation(annotation: Any, globalns: dict[str, Any]) -> Any:
    """
    Evaluates a type annotation, which can be a string or a ForwardRef.
    """
    pass


def get_typed_signature(call: Callable[..., Any]) -> inspect.Signature:
    """
    Returns a typed signature for a callable, resolving forward references.

    Parameters
    ----------
    call: Callable[..., Any]
        The callable to get the signature for

    Returns
    -------
    inspect.Signature
        The typed signature
    """
    pass


def get_path_param_names(path: str) -> set[str]:
    """
    Returns the path parameter names from a path template. Those are the strings between { and }.

    Parameters
    ----------
    path: str
        The path template

    Returns
    -------
    set[str]
        The path parameter names

    """
    pass


def get_dependant(
    *,
    path: str,
    call: Callable[..., Any],
    name: str | None = None,
    responses: dict[int, OpenAPIResponse] | None = None,
) -> Dependant:
    """
    Returns a dependant model for a handler function. A dependant model is a model that contains
    the parameters and return value of a handler function.

    Parameters
    ----------
    path: str
        The path template
    call: Callable[..., Any]
        The handler function
    name: str, optional
        The name of the handler function
    responses: list[dict[int, OpenAPIResponse]], optional
        The list of extra responses for the handler function

    Returns
    -------
    Dependant
        The dependant model for the handler function
    """
    pass


def _add_extra_responses(dependant: Dependant, responses: dict[int, OpenAPIResponse] | None):
    # Also add the optional extra responses to the dependant model.
    pass


def _add_return_annotation(dependant: Dependant, endpoint_signature: inspect.Signature):
    # If the return annotation is not empty, add it to the dependant model.
    pass


def is_body_param(*, param_field: ModelField, is_path_param: bool) -> bool:
    """
    Returns whether a parameter is a request body parameter, by checking if it is a scalar field or a body field.

    Parameters
    ----------
    param_field: ModelField
        The parameter field
    is_path_param: bool
        Whether the parameter is a path parameter

    Returns
    -------
    bool
        Whether the parameter is a request body parameter
    """
    pass


def get_flat_params(dependant: Dependant) -> list[ModelField]:
    """
    Get a list of all the parameters from a Dependant object.

    Parameters
    ----------
    dependant : Dependant
        The Dependant object containing the parameters.

    Returns
    -------
    list[ModelField]
        A list of ModelField objects containing the flat parameters from the Dependant object.

    """
    flat_dependant = get_flat_dependant(dependant)
    return (
        flat_dependant.path_params
        + flat_dependant.query_params
        + flat_dependant.header_params
        + flat_dependant.cookie_params
    )


def get_body_field(*, dependant: Dependant, name: str) -> ModelField | None:
    """
    Get the Body field for a given Dependant object.
    """
    pass


def get_body_field_info(
    *,
    body_model: type[BaseModel],
    flat_dependant: Dependant,
    required: bool,
) -> tuple[type[Body], dict[str, Any]]:
    """
    Get the Body field info and kwargs for a given body model.
    """
    pass
