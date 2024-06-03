from dataclasses import dataclass
from functools import partial
import inspect
from typing import Callable, Protocol, Any, TypeVar, dataclass_transform, final


class _Method(Protocol):
    __name__: str

    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


class _StruuuctifyCls(Protocol):
    __struuuctify__: dict[str, _Method]


def _struct_get_attr(self: _StruuuctifyCls, item: str) -> Callable[..., Any]:
    method = self.__struuuctify__.get(item, None)
    if method is None:
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")
    return partial(method, self)


T = TypeVar("T")


@dataclass_transform()
def struct(cls: type[T]) -> type[T]:
    setattr(cls, "__struuuctify__", {})

    setattr(cls, "__getattr__", _struct_get_attr)
    return final(dataclass(cls))


def impl(func: _Method) -> Callable[..., Any]:
    cls = func.__annotations__.get("self")
    if cls is None or not inspect.isclass(cls):
        raise TypeError("self attribute should be a struct class")

    cls.__struuuctify__[func.__name__] = func
    return func
