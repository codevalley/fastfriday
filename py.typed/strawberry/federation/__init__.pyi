from typing import Any, Callable, TypeVar, Type

T = TypeVar("T")

def lazy(fn: Callable[[], Type[T]]) -> Any: ...
