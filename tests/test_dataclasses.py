"""Tests for dataclass handler."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from rich.console import Group

from sus_inspector.hooks.dataclasses import DataclassHandler

F_COUNT_12: Final = 12


@dataclass
class SimpleDataclass:
    """Simple dataclass."""

    a: int
    b: str


@dataclass
class LargeDataclass:
    """Large dataclass."""

    f0: int = 0
    f1: int = 1
    f2: int = 2
    f3: int = 3
    f4: int = 4
    f5: int = 5
    f6: int = 6
    f7: int = 7
    f8: int = 8
    f9: int = 9
    f10: int = 10
    f11: int = 11


def test_dataclass_handler_can_handle() -> None:
    """Test can_handle method."""
    handler = DataclassHandler()
    simple = SimpleDataclass(1, "test")

    assert handler.can_handle(simple) is True
    assert handler.can_handle({"a": 1}) is False
    # Should not handle class itself
    assert handler.can_handle(SimpleDataclass) is False


def test_dataclass_handler_get_type_tag() -> None:
    """Test get_type_tag method."""
    handler = DataclassHandler()
    simple = SimpleDataclass(1, "test")
    assert handler.get_type_tag(simple) == "Dataclass"


def test_dataclass_handler_get_fields() -> None:
    """Test get_fields method."""
    handler = DataclassHandler()
    simple = SimpleDataclass(1, "test")
    fields = handler.get_fields(simple)
    assert fields == {"a": 1, "b": "test"}


def test_dataclass_handler_render() -> None:
    """Test render method."""
    handler = DataclassHandler()
    simple = SimpleDataclass(1, "test")
    renderable = handler.render(simple)
    assert isinstance(renderable, Group)

    # Complex object (many fields)
    large = LargeDataclass()
    renderable_complex = handler.render(large, expanded=False)
    # Check that it's a summary (contains "(12 fields) ...")
    assert f"({F_COUNT_12} fields) ..." in str(renderable_complex.renderables[1])

    # Expanded view
    renderable_expanded = handler.render(large, expanded=True)
    # Should not contain summary
    assert f"({F_COUNT_12} fields) ..." not in str(renderable_expanded.renderables[1])
