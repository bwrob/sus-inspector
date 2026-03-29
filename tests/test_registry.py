"""Tests for the hook registry system."""

from __future__ import annotations

from typing import Any

from rich.text import Text

from sus_inspector.hooks.inspector import CLASS_REGISTRY, INSTANCE_REGISTRY
from sus_inspector.hooks.registry import (
    CLASS_HOOKS,
    INSTANCE_HOOKS,
    get_renderer,
    register_class_hook,
    register_instance_hook,
)


def test_double_registry_lookup() -> None:
    """Test that looking up in different registries works."""

    def instance_view(obj: Any) -> Text:  # noqa: ANN401
        return Text(f"Instance: {obj}")

    def class_view(obj: Any) -> Text:  # noqa: ANN401
        return Text(f"Class: {obj}")

    class MyType:
        pass

    register_instance_hook(MyType, instance_view)
    register_class_hook(MyType, class_view)

    obj = MyType()

    renderer = get_renderer(obj, INSTANCE_HOOKS)
    assert renderer is not None
    # Check startswith to avoid long line length issues
    assert str(renderer(obj)).startswith("Instance: <tests.test_registry")

    renderer = get_renderer(obj, CLASS_HOOKS)
    assert renderer is not None
    assert str(renderer(obj)).startswith("Class: <tests.test_registry")


def test_fallback_logic() -> None:
    """Test that fallback works correctly (returns None if no hook)."""

    class MyType:
        pass

    INSTANCE_REGISTRY.inspectors.clear()
    CLASS_REGISTRY.inspectors.clear()

    obj = MyType()
    assert get_renderer(obj, INSTANCE_HOOKS) is None
    assert get_renderer(obj, CLASS_HOOKS) is None
