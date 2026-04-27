"""Lightweight dependency injection primitives — no pydantic import."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Any, get_args, get_origin, get_type_hints

if TYPE_CHECKING:
    from collections.abc import Callable

    from aws_lambda_powertools.event_handler.openapi.params import Dependant
    from aws_lambda_powertools.event_handler.request import Request


class DependencyResolutionError(Exception):
    """Raised when a dependency cannot be resolved."""


class Depends:
    """
    Declares a dependency for a route handler parameter.

    Dependencies are resolved automatically before the handler is called. The return value
    of the dependency callable is injected as the parameter value.

    Parameters
    ----------
    dependency: Callable[..., Any]
        A callable whose return value will be injected into the handler parameter.
        The callable can itself declare ``Depends()`` parameters to form a dependency tree.
    use_cache: bool
        If ``True`` (default), the dependency result is cached per invocation so that
        the same dependency used multiple times is only called once.

    Examples
    --------

    ```python
    from typing import Annotated

    from aws_lambda_powertools.event_handler import APIGatewayHttpResolver, Depends

    app = APIGatewayHttpResolver()

    def get_tenant() -> str:
        return "default-tenant"

    @app.get("/orders")
    def list_orders(tenant_id: Annotated[str, Depends(get_tenant)]):
        return {"tenant": tenant_id}
    ```
    """

    def __init__(self, dependency: Callable[..., Any], *, use_cache: bool = True) -> None:
        if not callable(dependency):
            raise DependencyResolutionError(
                f"Depends() requires a callable, got {type(dependency).__name__}: {dependency!r}",
            )
        self.dependency = dependency
        self.use_cache = use_cache


class _DependencyNode:
    """Lightweight node in a dependency tree — used by ``build_dependency_tree``."""

    def __init__(self, *, param_name: str, depends: Depends, sub_tree: DependencyTree) -> None:
        self.param_name = param_name
        self.depends = depends
        self.dependant = sub_tree


class DependencyTree:
    """Lightweight dependency tree — no pydantic required.

    This mirrors the shape that ``solve_dependencies`` expects (a ``.dependencies``
    attribute containing nodes with ``.param_name``, ``.depends``, and ``.dependant``),
    but can be built without importing pydantic.
    """

    def __init__(self, *, dependencies: list[_DependencyNode] | None = None) -> None:
        self.dependencies: list[_DependencyNode] = dependencies or []


class DependencyParam:
    """Holds a dependency's parameter name and its resolved Dependant sub-tree (OpenAPI path)."""

    def __init__(self, *, param_name: str, depends: Depends, dependant: Dependant) -> None:
        self.param_name = param_name
        self.depends = depends
        self.dependant = dependant


def _get_depends_from_annotation(annotation: Any) -> Depends | None:
    """Extract a Depends instance from an Annotated[Type, Depends(...)] annotation."""
    pass


def _has_depends(func: Callable[..., Any]) -> bool:
    """Check if a callable has any Depends() parameters, without importing pydantic."""
    pass


def build_dependency_tree(func: Callable[..., Any]) -> DependencyTree:
    """Build a lightweight dependency tree from a callable's signature.

    This inspects the function parameters for ``Annotated[Type, Depends(...)]``
    annotations and recursively builds the tree — all without importing pydantic.
    """
    pass


def solve_dependencies(
    *,
    dependant: Dependant | DependencyTree,
    request: Request | None = None,
    dependency_overrides: dict[Callable[..., Any], Callable[..., Any]] | None = None,
    dependency_cache: dict[Callable[..., Any], Any] | None = None,
) -> dict[str, Any]:
    """
    Recursively resolve all ``Depends()`` parameters for a given dependant.

    Parameters
    ----------
    dependant: Dependant
        The dependant model containing dependency declarations
    request: Request, optional
        The current request object, injected into dependencies that declare a Request parameter
    dependency_overrides: dict, optional
        Mapping of original dependency callable to override callable (for testing)
    dependency_cache: dict, optional
        Per-invocation cache of resolved dependency values

    Returns
    -------
    dict[str, Any]
        Mapping of parameter name to resolved dependency value
    """
    pass
