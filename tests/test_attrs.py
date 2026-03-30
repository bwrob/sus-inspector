"""Tests for attrs specialized handler."""

from __future__ import annotations

from typing import Final

import attr
from rich.console import Group

from sus_inspector.hooks.attrs import AttrsHandler

F_COUNT_12: Final = 12


@attr.s
class SimpleAttr:
    """Simple attrs class."""

    a: int = attr.ib()
    b: str = attr.ib()


@attr.s
class LargeAttr:
    """Large attrs class."""

    f0: int = attr.ib(default=0)
    f1: int = attr.ib(default=0)
    f2: int = attr.ib(default=0)
    f3: int = attr.ib(default=0)
    f4: int = attr.ib(default=0)
    f5: int = attr.ib(default=0)
    f6: int = attr.ib(default=0)
    f7: int = attr.ib(default=0)
    f8: int = attr.ib(default=0)
    f9: int = attr.ib(default=0)
    f10: int = attr.ib(default=0)
    f11: int = attr.ib(default=0)


def test_attrs_handler_can_handle() -> None:
    """Test can_handle method."""
    handler = AttrsHandler()
    simple = SimpleAttr(a=1, b="test")

    assert handler.can_handle(simple) is True
    assert handler.can_handle({"a": 1}) is False
    assert handler.can_handle(SimpleAttr) is False


def test_attrs_handler_get_type_tag() -> None:
    """Test get_type_tag method."""
    handler = AttrsHandler()
    simple = SimpleAttr(a=1, b="test")
    assert handler.get_type_tag(simple) == "Attrs"


def test_attrs_handler_get_fields() -> None:
    """Test get_fields method."""
    handler = AttrsHandler()
    simple = SimpleAttr(a=1, b="test")
    fields = handler.get_fields(simple)
    assert fields == {"a": 1, "b": "test"}


def test_attrs_handler_render() -> None:
    """Test render method."""
    handler = AttrsHandler()
    simple = SimpleAttr(a=1, b="test")
    renderable = handler.render(simple)
    assert isinstance(renderable, Group)

    # Complex object
    large = LargeAttr()
    renderable_complex = handler.render(large, expanded=False)
    assert f"({F_COUNT_12} fields) ..." in str(renderable_complex.renderables[1])
