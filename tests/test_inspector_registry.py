"""Tests for the InspectorRegistry."""

from rich.text import Text
from sus_inspector.hooks.inspector import InspectorRegistry


def test_registry_register_type():
    """Test registering an inspector for a specific type."""
    registry = InspectorRegistry()

    def int_inspector(obj: int):
        return Text(f"Int: {obj}")

    registry.register(int, int_inspector)

    inspector = registry.get_inspector(10)
    assert inspector == int_inspector
    assert str(inspector(10)) == "Int: 10"


def test_registry_register_condition():
    """Test registering an inspector for a condition."""
    registry = InspectorRegistry()

    def string_inspector(obj: str):
        return Text(f"String: {obj}")

    registry.register(lambda x: isinstance(x, str), string_inspector)

    inspector = registry.get_inspector("hello")
    assert inspector == string_inspector
    assert str(inspector("hello")) == "String: hello"


def test_registry_priority():
    """Test that the most recently registered inspector has priority."""
    registry = InspectorRegistry()

    def inspector1(obj: int):
        return Text(f"I1: {obj}")

    def inspector2(obj: int):
        return Text(f"I2: {obj}")

    registry.register(int, inspector1)
    registry.register(int, inspector2)

    inspector = registry.get_inspector(10)
    assert inspector == inspector2
    assert str(inspector(10)) == "I2: 10"


def test_registry_no_match():
    """Test that None is returned if no inspector matches."""
    registry = InspectorRegistry()
    assert registry.get_inspector(10) is None
