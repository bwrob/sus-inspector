"""Tests for specialized object handlers."""

from __future__ import annotations

from typing import Any

from rich.text import Text
from typing_extensions import override

from sus_inspector.hooks.base import BaseObjectHandler
from sus_inspector.hooks.handlers import (
    HANDLER_REGISTRY,
    HandlerRegistry,
    ensure_handlers,
)


class MockHandler(BaseObjectHandler):
    """Mock handler for testing."""

    @override
    def can_handle(self, obj: Any) -> bool:
        """Mock implementation.

        Returns:
            bool: True if dictionary contains __mock__.

        """
        return isinstance(obj, dict) and "__mock__" in obj

    @override
    def get_type_tag(self, obj: Any) -> str:
        """Mock implementation.

        Returns:
            str: "Mock"

        """
        return "Mock"

    @override
    def get_fields(self, obj: Any) -> dict[str, Any]:
        """Mock implementation.

        Returns:
            dict[str, Any]: Mock fields.

        """
        return {k: v for k, v in obj.items() if k != "__mock__"}

    @override
    def render(self, obj: Any, *, expanded: bool = False) -> Text:
        """Mock implementation.

        Returns:
            Text: Mock text.

        """
        return Text("Mock Object")


def test_handler_registry() -> None:
    """Test the handler registry."""
    registry = HandlerRegistry()
    handler = MockHandler()
    registry.register(handler)

    mock_obj = {"__mock__": True, "field1": "value1"}
    other_obj = {"field1": "value1"}

    assert registry.get_handler(mock_obj) is handler
    assert registry.get_handler(other_obj) is None


def test_base_object_handler_is_complex() -> None:
    """Test the default is_complex implementation."""
    handler = MockHandler()

    simple_obj = {"__mock__": True, **{f"field{i}": i for i in range(5)}}
    complex_obj = {"__mock__": True, **{f"field{i}": i for i in range(15)}}

    assert handler.is_complex(simple_obj) is False
    assert handler.is_complex(complex_obj) is True


def test_global_handler_registry() -> None:
    """Test the global handler registry exists."""
    assert isinstance(HANDLER_REGISTRY, HandlerRegistry)


def test_ensure_handlers() -> None:
    """Test the ensure_handlers function."""
    ensure_handlers()
    # Should not crash, and should be idempotent if called again
    ensure_handlers()
