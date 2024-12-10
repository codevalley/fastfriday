"""Type stubs for Strawberry lazy type resolution."""

from typing import Any, Callable, TypeVar, Type

T = TypeVar("T")

def lazy(fn: Callable[[], Type[T]]) -> Any: ...
