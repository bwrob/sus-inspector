"""Tests for msgspec specialized handler."""

from __future__ import annotations

from typing import Final

import msgspec
from rich.console import Group

from sus_inspector.hooks.msgspec import MsgspecHandler

F_COUNT_12: Final = 12


class SimpleStruct(msgspec.Struct):
    """Simple msgspec struct."""

    a: int
    b: str


class LargeStruct(msgspec.Struct):
    """Large msgspec struct."""

    f0: int = 0
    f1: int = 0
    f2: int = 0
    f3: int = 0
    f4: int = 0
    f5: int = 0
    f6: int = 0
    f7: int = 0
    f8: int = 0
    f9: int = 0
    f10: int = 0
    f11: int = 0


def test_msgspec_handler_can_handle() -> None:
    """Test can_handle method."""
    handler = MsgspecHandler()
    simple = SimpleStruct(a=1, b="test")

    assert handler.can_handle(simple) is True
    assert handler.can_handle({"a": 1}) is False
    assert handler.can_handle(SimpleStruct) is False


def test_msgspec_handler_get_type_tag() -> None:
    """Test get_type_tag method."""
    handler = MsgspecHandler()
    simple = SimpleStruct(a=1, b="test")
    assert handler.get_type_tag(simple) == "Msgspec"


def test_msgspec_handler_get_fields() -> None:
    """Test get_fields method."""
    handler = MsgspecHandler()
    simple = SimpleStruct(a=1, b="test")
    fields = handler.get_fields(simple)
    assert fields == {"a": 1, "b": "test"}


def test_msgspec_handler_render() -> None:
    """Test render method."""
    handler = MsgspecHandler()
    simple = SimpleStruct(a=1, b="test")
    renderable = handler.render(simple)
    assert isinstance(renderable, Group)

    # Complex object
    large = LargeStruct()
    renderable_complex = handler.render(large, expanded=False)
    assert f"({F_COUNT_12} fields) ..." in str(renderable_complex.renderables[1])
