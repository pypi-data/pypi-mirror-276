from typing import Callable, Any

import pytest

from structify import struct, impl
from .incorrect_function import add_1, add_2


def test_struuuctify() -> None:
    @struct
    class Point:
        x: float
        y: float

    @impl
    def add(
        self: Point,
    ) -> float:
        return self.x + self.y

    p = Point(1, 2)

    assert p.add() == 3  # type: ignore


def test_struuuctify_args() -> None:
    @struct
    class Point:
        x: int
        y: int

    @impl
    def a(self: Point, *args: int) -> int:
        return self.x + self.y + sum(args)

    @impl
    def b(self: Point, *args: int, **kwargs: int) -> int:
        return self.x + self.y + sum(args) + sum(kwargs.values())

    p = Point(1, 2)

    assert p.a(3, 4) == 10  # type: ignore
    assert p.b(3, 4, x=5, y=6) == 21  # type: ignore


@pytest.mark.parametrize("func", [add_1, add_2])
def test_struuuctify_impl_with_no_self(func: Callable[..., Any]) -> None:
    with pytest.raises(TypeError, match="self attribute should be a struct"):
        impl(func)


def test_struuuctify_raise_attribute_error() -> None:
    @struct
    class Point:
        x: float
        y: float

    p = Point(1, 2)

    with pytest.raises(AttributeError, match="'Point' object has no attribute 'missing_attribute'"):
        p.missing_attribute  # type: ignore[attr-defined]
