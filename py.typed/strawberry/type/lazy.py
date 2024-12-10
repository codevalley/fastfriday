"""Lazy type resolution for Strawberry."""

from typing import Any, Callable, TypeVar, Type


T = TypeVar("T")


def lazy(fn: Callable[[], Type[T]]) -> Any:
    """Create a lazy type reference."""
    return fn
