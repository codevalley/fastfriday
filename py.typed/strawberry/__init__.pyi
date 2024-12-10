"""Type stubs for Strawberry core functionality."""

from typing import (
    Any,
    Callable,
    TypeVar,
    Optional,
    Type,
    TypeVar,
    Union,
    Dict,
)

from .type import lazy
from .scalars import JSON

T = TypeVar("T")

def type(cls: Type[T]) -> Type[T]: ...
def field(
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    default: Any = None,
    default_factory: Optional[Callable[[], Any]] = None,
    deprecation_reason: Optional[str] = None,
    permission_classes: Any = (),
    directives: Any = (),
) -> Any: ...
def input(cls: Type[T]) -> Type[T]: ...

__all__ = [
    "type",
    "field",
    "input",
    "lazy",
    "JSON",
]
