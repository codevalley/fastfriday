"""Strawberry GraphQL type stubs."""

from typing import (
    Any,
    Callable,
    TypeVar,
    Optional,
    Type,
    Union,
    Dict,
)

from .type import lazy
from .scalars import JSON

T = TypeVar("T")


def type(cls: Type[T]) -> Type[T]:
    """Decorator to mark a class as a GraphQL type."""
    return cls


def field(
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    default: Any = None,
    default_factory: Optional[Callable[[], Any]] = None,
    deprecation_reason: Optional[str] = None,
    permission_classes: Any = (),
    directives: Any = (),
) -> Any:
    """Decorator to mark a field as a GraphQL field."""
    return lambda x: x


def input(cls: Type[T]) -> Type[T]:
    """Decorator to mark a class as a GraphQL input type."""
    return cls


__all__ = [
    "type",
    "field",
    "input",
    "lazy",
    "JSON",
]
