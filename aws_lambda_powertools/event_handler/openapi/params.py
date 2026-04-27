from __future__ import annotations

import inspect
from enum import Enum
from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseConfig, BaseModel, create_model
from pydantic.fields import FieldInfo
from typing_extensions import Annotated, get_args, get_origin

from aws_lambda_powertools.event_handler import Response
from aws_lambda_powertools.event_handler.openapi.compat import (
    ModelField,
    Required,
    Undefined,
    UndefinedType,
    copy_field_info,
    field_annotation_is_scalar,
    get_annotation_from_field_info,
    lenient_issubclass,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from aws_lambda_powertools.event_handler.depends import DependencyParam
    from aws_lambda_powertools.event_handler.openapi.models import Example
    from aws_lambda_powertools.event_handler.openapi.types import CacheKey

"""
This turns the low-level function signature into typed, validated Pydantic models for consumption.
"""


class ParamTypes(Enum):
    query = "query"
    header = "header"
    path = "path"
    cookie = "cookie"


# MAINTENANCE: update when deprecating Pydantic v1, remove this alias
_Unset: Any = Undefined


class Dependant:
    """
    A class used internally to represent a dependency between path operation decorators and the path operation function.
    """

    def __init__(
        self,
        *,
        path_params: list[ModelField] | None = None,
        query_params: list[ModelField] | None = None,
        header_params: list[ModelField] | None = None,
        cookie_params: list[ModelField] | None = None,
        body_params: list[ModelField] | None = None,
        return_param: ModelField | None = None,
        response_extra_models: list[ModelField] | None = None,
        name: str | None = None,
        call: Callable[..., Any] | None = None,
        request_param_name: str | None = None,
        websocket_param_name: str | None = None,
        http_connection_param_name: str | None = None,
        response_param_name: str | None = None,
        background_tasks_param_name: str | None = None,
        dependencies: list[DependencyParam] | None = None,
        path: str | None = None,
    ) -> None:
        self.path_params = path_params or []
        self.query_params = query_params or []
        self.header_params = header_params or []
        self.cookie_params = cookie_params or []
        self.body_params = body_params or []
        self.return_param = return_param or None
        self.response_extra_models = response_extra_models or []
        self.request_param_name = request_param_name
        self.websocket_param_name = websocket_param_name
        self.http_connection_param_name = http_connection_param_name
        self.response_param_name = response_param_name
        self.background_tasks_param_name = background_tasks_param_name
        self.dependencies = dependencies or []
        self.name = name
        self.call = call
        # Store the path to be able to re-generate a dependable from it in overrides
        self.path = path
        # Save the cache key at creation to optimize performance
        self.cache_key: CacheKey = self.call


class Param(FieldInfo):  # type: ignore[misc]
    """
    A class used internally to represent a parameter in a path operation.
    """

    in_: ParamTypes

    def __init__(
        self,
        default: Any = Undefined,
        *,
        default_factory: Callable[[], Any] | None = _Unset,
        annotation: Any | None = None,
        alias: str | None = None,
        alias_priority: int | None = _Unset,
        # MAINTENANCE: update when deprecating Pydantic v1, import these types
        # MAINTENANCE: validation_alias: str | AliasPath | AliasChoices | None
        validation_alias: str | None = _Unset,
        serialization_alias: str | None = None,
        title: str | None = None,
        description: str | None = None,
        gt: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        le: float | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | None = None,
        discriminator: str | None = None,
        strict: bool | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        examples: list[Any] | None = None,
        openapi_examples: dict[str, Example] | None = None,
        deprecated: bool | None = None,
        include_in_schema: bool = True,
        json_schema_extra: dict[str, Any] | None = None,
        **extra: Any,
    ):
        """
        Constructs a new Param.

        Parameters
        ----------
        default: Any
            The default value of the parameter
        default_factory: Callable[[], Any], optional
            Callable that will be called when a default value is needed for this field
        annotation: Any, optional
            The type annotation of the parameter
        alias: str, optional
            The public name of the field
        alias_priority: int, optional
            Priority of the alias. This affects whether an alias generator is used
        validation_alias: str | AliasPath | AliasChoices | None, optional
            Alias to be used for validation only
        serialization_alias: str | AliasPath | AliasChoices | None, optional
            Alias to be used for serialization only
        title: str, optional
            The title of the parameter
        description: str, optional
            The description of the parameter
        gt: float, optional
            Only applies to numbers, required the field to be "greater than"
        ge: float, optional
            Only applies to numbers, required the field to be "greater than or equal"
        lt: float, optional
            Only applies to numbers, required the field to be "less than"
        le: float, optional
            Only applies to numbers, required the field to be "less than or equal"
        min_length: int, optional
            Only applies to strings, required the field to have a minimum length
        max_length: int, optional
            Only applies to strings, required the field to have a maximum length
        pattern: str, optional
            Only applies to strings, requires the field match against a regular expression pattern string
        discriminator: str, optional
            Parameter field name for discriminating the type in a tagged union
        strict: bool, optional
            Enables Pydantic's strict mode for the field
        multiple_of: float, optional
            Only applies to numbers, requires the field to be a multiple of the given value
        allow_inf_nan: bool, optional
            Only applies to numbers, requires the field to allow infinity and NaN values
        max_digits: int, optional
            Only applies to Decimals, requires the field to have a maxmium number of digits within the decimal.
        decimal_places: int, optional
            Only applies to Decimals, requires the field to have at most a number of decimal places
        examples: list[Any], optional
            A list of examples for the parameter
        deprecated: bool, optional
            If `True`, the parameter will be marked as deprecated
        include_in_schema: bool, optional
            If `False`, the parameter will be excluded from the generated OpenAPI schema
        json_schema_extra: dict[str, Any], optional
            Extra values to include in the generated OpenAPI schema
        """
        self.deprecated = deprecated
        self.include_in_schema = include_in_schema

        kwargs = dict(
            default=default,
            default_factory=default_factory,
            alias=alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            discriminator=discriminator,
            multiple_of=multiple_of,
            allow_nan=allow_inf_nan,
            max_digits=max_digits,
            decimal_places=decimal_places,
            **extra,
        )
        if examples is not None:
            kwargs["examples"] = examples

        if openapi_examples is not None:
            kwargs["openapi_examples"] = openapi_examples

        current_json_schema_extra = json_schema_extra or extra

        self.openapi_examples = openapi_examples

        # Pydantic 2.12+ no longer copies alias to validation_alias automatically
        # Ensure alias and validation_alias are in sync when only one is provided
        if validation_alias is _Unset and alias is not None:
            validation_alias = alias
        elif alias is None and validation_alias is not _Unset and validation_alias is not None:
            alias = validation_alias
            kwargs["alias"] = alias

        kwargs.update(
            {
                "annotation": annotation,
                "alias_priority": alias_priority,
                "validation_alias": validation_alias,
                "serialization_alias": serialization_alias,
                "strict": strict,
                "json_schema_extra": current_json_schema_extra,
                "pattern": pattern,
            },
        )

        use_kwargs = {k: v for k, v in kwargs.items() if v is not _Unset}

        super().__init__(**use_kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.default})"


class Path(Param):  # type: ignore[misc]
    """
    A class used internally to represent a path parameter in a path operation.
    """

    in_ = ParamTypes.path

    def __init__(
        self,
        default: Any = ...,
        *,
        default_factory: Callable[[], Any] | None = _Unset,
        annotation: Any | None = None,
        alias: str | None = None,
        alias_priority: int | None = _Unset,
        # MAINTENANCE: update when deprecating Pydantic v1, import these types
        # MAINTENANCE: validation_alias: str | AliasPath | AliasChoices | None
        validation_alias: str | None = _Unset,
        serialization_alias: str | None = None,
        title: str | None = None,
        description: str | None = None,
        gt: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        le: float | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | None = None,
        discriminator: str | None = None,
        strict: bool | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        examples: list[Any] | None = None,
        openapi_examples: dict[str, Example] | None = None,
        deprecated: bool | None = None,
        include_in_schema: bool = True,
        json_schema_extra: dict[str, Any] | None = None,
        **extra: Any,
    ):
        if default is not ...:
            raise AssertionError("Path parameters cannot have a default value")

        super().__init__(
            default=default,
            default_factory=default_factory,
            annotation=annotation,
            alias=alias,
            alias_priority=alias_priority,
            validation_alias=validation_alias,
            serialization_alias=serialization_alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            discriminator=discriminator,
            strict=strict,
            multiple_of=multiple_of,
            allow_inf_nan=allow_inf_nan,
            max_digits=max_digits,
            decimal_places=decimal_places,
            deprecated=deprecated,
            examples=examples,
            openapi_examples=openapi_examples,
            include_in_schema=include_in_schema,
            json_schema_extra=json_schema_extra,
            **extra,
        )


class Query(Param):  # type: ignore[misc]
    """
    A class used internally to represent a query parameter in a path operation.
    """

    in_ = ParamTypes.query

    def __init__(
        self,
        default: Any = _Unset,
        *,
        default_factory: Callable[[], Any] | None = _Unset,
        annotation: Any | None = None,
        alias: str | None = None,
        alias_priority: int | None = _Unset,
        validation_alias: str | None = _Unset,
        serialization_alias: str | None = None,
        title: str | None = None,
        description: str | None = None,
        gt: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        le: float | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | None = None,
        discriminator: str | None = None,
        strict: bool | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        examples: list[Any] | None = None,
        openapi_examples: dict[str, Example] | None = None,
        deprecated: bool | None = None,
        include_in_schema: bool = True,
        json_schema_extra: dict[str, Any] | None = None,
        **extra: Any,
    ):
        super().__init__(
            default=default,
            default_factory=default_factory,
            annotation=annotation,
            alias=alias,
            alias_priority=alias_priority,
            validation_alias=validation_alias,
            serialization_alias=serialization_alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            discriminator=discriminator,
            strict=strict,
            multiple_of=multiple_of,
            allow_inf_nan=allow_inf_nan,
            max_digits=max_digits,
            decimal_places=decimal_places,
            deprecated=deprecated,
            examples=examples,
            openapi_examples=openapi_examples,
            include_in_schema=include_in_schema,
            json_schema_extra=json_schema_extra,
            **extra,
        )


class Header(Param):  # type: ignore[misc]
    """
    A class used internally to represent a header parameter in a path operation.
    """

    in_ = ParamTypes.header

    def __init__(
        self,
        default: Any = Undefined,
        *,
        default_factory: Callable[[], Any] | None = _Unset,
        annotation: Any | None = None,
        alias: str | None = None,
        alias_priority: int | None = _Unset,
        # MAINTENANCE: update when deprecating Pydantic v1, import these types
        # str | AliasPath | AliasChoices | None
        validation_alias: str | None = _Unset,
        serialization_alias: str | None = None,
        convert_underscores: bool = True,
        title: str | None = None,
        description: str | None = None,
        gt: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        le: float | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | None = None,
        discriminator: str | None = None,
        strict: bool | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        examples: list[Any] | None = None,
        openapi_examples: dict[str, Example] | None = None,
        deprecated: bool | None = None,
        include_in_schema: bool = True,
        json_schema_extra: dict[str, Any] | None = None,
        **extra: Any,
    ):
        self.convert_underscores = convert_underscores
        self._alias = alias

        super().__init__(
            default=default,
            default_factory=default_factory,
            annotation=annotation,
            alias=self._alias,
            alias_priority=alias_priority,
            validation_alias=validation_alias,
            serialization_alias=serialization_alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            discriminator=discriminator,
            strict=strict,
            multiple_of=multiple_of,
            allow_inf_nan=allow_inf_nan,
            max_digits=max_digits,
            decimal_places=decimal_places,
            deprecated=deprecated,
            examples=examples,
            openapi_examples=openapi_examples,
            include_in_schema=include_in_schema,
            json_schema_extra=json_schema_extra,
            **extra,
        )

    @property
    def alias(self):
        pass

    @alias.setter
    def alias(self, value: str | None = None):
        pass


class Cookie(Param):  # type: ignore[misc]
    """
    A class used internally to represent a cookie parameter in a path operation.
    """

    in_ = ParamTypes.cookie


class Body(FieldInfo):  # type: ignore[misc]
    """
    A class used internally to represent a body parameter in a path operation.
    """

    def __init__(
        self,
        default: Any = Undefined,
        *,
        default_factory: Callable[[], Any] | None = _Unset,
        annotation: Any | None = None,
        embed: bool = False,
        media_type: str = "application/json",
        alias: str | None = None,
        alias_priority: int | None = _Unset,
        # MAINTENANCE: update when deprecating Pydantic v1, import these types
        # str | AliasPath | AliasChoices | None
        validation_alias: str | None = _Unset,
        serialization_alias: str | None = None,
        title: str | None = None,
        description: str | None = None,
        gt: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        le: float | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | None = None,
        discriminator: str | None = None,
        strict: bool | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        examples: list[Any] | None = None,
        openapi_examples: dict[str, Example] | None = None,
        deprecated: bool | None = None,
        include_in_schema: bool = True,
        json_schema_extra: dict[str, Any] | None = None,
        **extra: Any,
    ):
        self.embed = embed
        self.media_type = media_type
        self.deprecated = deprecated
        self.include_in_schema = include_in_schema
        kwargs = dict(
            default=default,
            default_factory=default_factory,
            alias=alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            discriminator=discriminator,
            multiple_of=multiple_of,
            allow_nan=allow_inf_nan,
            max_digits=max_digits,
            decimal_places=decimal_places,
            **extra,
        )
        if examples is not None:
            kwargs["examples"] = examples
        if openapi_examples is not None:
            kwargs["openapi_examples"] = openapi_examples
        current_json_schema_extra = json_schema_extra or extra

        # Pydantic 2.12+ no longer copies alias to validation_alias automatically
        # Ensure alias and validation_alias are in sync when only one is provided
        if validation_alias is _Unset and alias is not None:
            validation_alias = alias
        elif alias is None and validation_alias is not _Unset and validation_alias is not None:
            alias = validation_alias
            kwargs["alias"] = alias
        self.openapi_examples = openapi_examples

        kwargs.update(
            {
                "annotation": annotation,
                "alias_priority": alias_priority,
                "validation_alias": validation_alias,
                "serialization_alias": serialization_alias,
                "strict": strict,
                "json_schema_extra": current_json_schema_extra,
                "pattern": pattern,
            },
        )

        use_kwargs = {k: v for k, v in kwargs.items() if v is not _Unset}

        super().__init__(**use_kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.default})"


class Form(Body):  # type: ignore[misc]
    """
    A class used to represent a form parameter in a path operation.
    """

    def __init__(
        self,
        default: Any = Undefined,
        *,
        default_factory: Callable[[], Any] | None = _Unset,
        annotation: Any | None = None,
        media_type: str = "application/x-www-form-urlencoded",
        alias: str | None = None,
        alias_priority: int | None = _Unset,
        # MAINTENANCE: update when deprecating Pydantic v1, import these types
        # str | AliasPath | AliasChoices | None
        validation_alias: str | None = _Unset,
        serialization_alias: str | None = None,
        title: str | None = None,
        description: str | None = None,
        gt: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        le: float | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | None = None,
        discriminator: str | None = None,
        strict: bool | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        examples: list[Any] | None = None,
        deprecated: bool | None = None,
        include_in_schema: bool = True,
        json_schema_extra: dict[str, Any] | None = None,
        **extra: Any,
    ):
        super().__init__(
            default=default,
            default_factory=default_factory,
            annotation=annotation,
            embed=True,
            media_type=media_type,
            alias=alias,
            alias_priority=alias_priority,
            validation_alias=validation_alias,
            serialization_alias=serialization_alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            discriminator=discriminator,
            strict=strict,
            multiple_of=multiple_of,
            allow_inf_nan=allow_inf_nan,
            max_digits=max_digits,
            decimal_places=decimal_places,
            deprecated=deprecated,
            examples=examples,
            include_in_schema=include_in_schema,
            json_schema_extra=json_schema_extra,
            **extra,
        )


class UploadFile:
    """
    Represents an uploaded file with its metadata.

    Use with ``Annotated[UploadFile, File()]`` to receive file content along with
    filename and content type. For raw bytes only, use ``Annotated[bytes, File()]``.

    Attributes
    ----------
    filename : str | None
        The original filename from the upload.
    content_type : str | None
        The MIME type declared by the client (e.g. ``image/jpeg``).
    content : bytes
        The raw file content.
    """

    __slots__ = ("content", "content_type", "filename")

    def __init__(self, *, content: bytes, filename: str | None = None, content_type: str | None = None):
        self.content = content
        self.filename = filename
        self.content_type = content_type

    def __len__(self) -> int:
        return len(self.content)

    def __repr__(self) -> str:
        return f"UploadFile(filename={self.filename!r}, content_type={self.content_type!r}, size={len(self.content)})"

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> Any:
        from pydantic_core import core_schema

        return core_schema.no_info_plain_validator_function(
            cls._validate,
            serialization=core_schema.plain_serializer_function_ser_schema(lambda v: v, info_arg=False),
        )

    @classmethod
    def _validate(cls, v: Any) -> UploadFile:
        pass

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema: Any, handler: Any) -> dict[str, Any]:
        return {"type": "string", "format": "binary"}


class File(Form):  # type: ignore[misc]
    """
    A class used to represent a file parameter in a path operation.
    """

    def __init__(
        self,
        default: Any = Undefined,
        *,
        default_factory: Callable[[], Any] | None = _Unset,
        annotation: Any | None = None,
        media_type: str = "multipart/form-data",
        alias: str | None = None,
        alias_priority: int | None = _Unset,
        # MAINTENANCE: update when deprecating Pydantic v1, import these types
        # str | AliasPath | AliasChoices | None
        validation_alias: str | None = None,
        serialization_alias: str | None = None,
        title: str | None = None,
        description: str | None = None,
        gt: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        le: float | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | None = None,
        discriminator: str | None = None,
        strict: bool | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        examples: list[Any] | None = None,
        deprecated: bool | None = None,
        include_in_schema: bool = True,
        json_schema_extra: dict[str, Any] | None = None,
        **extra: Any,
    ):
        # For file uploads, ensure the OpenAPI schema has the correct format
        # Also we can't test it
        file_schema_extra = {"format": "binary"}  # pragma: no cover
        if json_schema_extra:  # pragma: no cover
            json_schema_extra.update(file_schema_extra)  # pragma: no cover
        else:  # pragma: no cover
            json_schema_extra = file_schema_extra  # pragma: no cover

        super().__init__(
            default=default,
            default_factory=default_factory,
            annotation=annotation,
            media_type=media_type,
            alias=alias,
            alias_priority=alias_priority,
            validation_alias=validation_alias,
            serialization_alias=serialization_alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            discriminator=discriminator,
            strict=strict,
            multiple_of=multiple_of,
            allow_inf_nan=allow_inf_nan,
            max_digits=max_digits,
            decimal_places=decimal_places,
            deprecated=deprecated,
            examples=examples,
            include_in_schema=include_in_schema,
            json_schema_extra=json_schema_extra,
            **extra,
        )


def get_flat_dependant(
    dependant: Dependant,
    visited: list[CacheKey] | None = None,
) -> Dependant:
    """
    Flatten a recursive Dependant model structure.

    This function recursively concatenates the parameter fields of a Dependant model and its dependencies into a flat
    Dependant structure. This is useful for scenarios like parameter validation where the nested structure is not
    relevant.

    Parameters
    ----------
    dependant: Dependant
        The dependant model to flatten
    visited: list[CacheKey], optional
        Keeps track of visited Dependents to avoid infinite recursion. Defaults to empty list.

    Returns
    -------
    Dependant
        The flattened Dependant model
    """
    if visited is None:
        visited = []
    visited.append(dependant.cache_key)

    flat = Dependant(
        path_params=dependant.path_params.copy(),
        query_params=dependant.query_params.copy(),
        header_params=dependant.header_params.copy(),
        cookie_params=dependant.cookie_params.copy(),
        body_params=dependant.body_params.copy(),
        path=dependant.path,
    )

    # Flatten sub-dependencies that declare HTTP params (query, header, etc.)
    for dep in dependant.dependencies:
        if dep.dependant.cache_key not in visited:
            sub_flat = get_flat_dependant(dep.dependant, visited=visited)
            flat.path_params.extend(sub_flat.path_params)
            flat.query_params.extend(sub_flat.query_params)
            flat.header_params.extend(sub_flat.header_params)
            flat.cookie_params.extend(sub_flat.cookie_params)
            flat.body_params.extend(sub_flat.body_params)

    return flat


def analyze_param(
    *,
    param_name: str,
    annotation: Any,
    value: Any,
    is_path_param: bool,
    is_response_param: bool,
) -> ModelField | None:
    """
    Analyze a parameter annotation and value to determine the type and default value of the parameter.

    Parameters
    ----------
    param_name: str
        The name of the parameter
    annotation
        The annotation of the parameter
    value
        The value of the parameter
    is_path_param
        Whether the parameter is a path parameter
    is_response_param
        Whether the parameter is the return annotation

    Returns
    -------
    ModelField | None
        The type annotation and the Pydantic field representing the parameter
    """
    pass


def get_field_info_and_type_annotation(
    annotation,
    value,
    is_path_param: bool,
    is_response_param: bool,
) -> tuple[FieldInfo | None, Any]:
    """
    Get the FieldInfo and type annotation from an annotation and value.
    """
    pass


def get_field_info_tuple_type(annotation, value) -> tuple[FieldInfo | None, Any]:
    pass


def get_field_info_response_type(annotation, value) -> tuple[FieldInfo | None, Any]:
    # Example: get_args(Response[inner_type]) == (inner_type,)  # noqa: ERA001
    pass


def _has_discriminator(field_info: FieldInfo) -> bool:
    """Check if a FieldInfo has a discriminator."""
    pass


def _handle_discriminator_with_param(
    annotations: list[FieldInfo],
    annotation: Any,
) -> tuple[FieldInfo | None, Any, bool]:
    """
    Handle the special case of Field(discriminator) + Body() combination.

    Returns:
        tuple of (powertools_annotation, type_annotation, has_discriminator_with_body)
    """
    pass


def _create_field_info(
    powertools_annotation: FieldInfo,
    type_annotation: Any,
    has_discriminator_with_body: bool,
) -> FieldInfo:
    """Create or copy FieldInfo based on the annotation type."""
    pass


def _set_field_default(field_info: FieldInfo, value: Any, is_path_param: bool) -> None:
    """Set the default value for a field."""
    pass


def get_field_info_annotated_type(annotation, value, is_path_param: bool) -> tuple[FieldInfo | None, Any]:
    """
    Get the FieldInfo and type annotation from an Annotated type.
    """
    pass


def create_response_field(
    name: str,
    type_: type[Any],
    default: Any | None = Undefined,
    required: bool | UndefinedType = Undefined,
    model_config: type[BaseConfig] = BaseConfig,
    field_info: FieldInfo | None = None,
    alias: str | None = None,
    mode: Literal["validation", "serialization"] = "validation",
) -> ModelField:
    """
    Create a new response field. Raises if type_ is invalid.
    """
    pass


def _apply_header_underscore_conversion(
    field_info: FieldInfo,
    type_annotation: Any,
    param_name: str,
) -> tuple[FieldInfo, Any]:
    """
    Apply underscore-to-dash conversion for Header parameters.

    For BaseModel: Creates new model with underscore-to-dash alias generator.
    Note: If the BaseModel already has an alias generator, it will be replaced
    with dash-case conversion since HTTP headers should use dash-case.
    For all Header fields: Sets the parameter alias if convert_underscores is True
    """
    pass


def _create_model_field(
    field_info: FieldInfo | None,
    type_annotation: Any,
    param_name: str,
    is_path_param: bool,
) -> ModelField | None:
    """
    Create a new ModelField from a FieldInfo and type annotation.
    """
    pass
