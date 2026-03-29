"""Tests for the hook registry system."""

from __future__ import annotations

from typing import Any, cast

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
    """Test that instance and class registries can have different hooks."""

    class MyType:
        pass

    def instance_renderer(_obj: Any) -> Text:  # noqa: ANN401
        return Text("Instance")

    def class_renderer(_obj: Any) -> Text:  # noqa: ANN401
        return Text("Class")

    # Clear hooks for test
    INSTANCE_HOOKS.clear()
    CLASS_HOOKS.clear()

    register_instance_hook(MyType, instance_renderer)
    register_class_hook(MyType, class_renderer)

    obj = MyType()

    # Test instance lookup
    inst_render = get_renderer(obj, INSTANCE_HOOKS)
    assert inst_render == instance_renderer
    if inst_render:
        res = inst_render(obj)
        label = cast("Text", res)
        assert label.plain == "Instance"

    # Test class lookup
    class_render = get_renderer(obj, CLASS_HOOKS)
    assert class_render == class_renderer
    if class_render:
        res = class_render(obj)
        label = cast("Text", res)
        assert label.plain == "Class"


def test_fallback_logic() -> None:
    """Test that fallback works correctly (returns None if no hook)."""

    class MyType:
        pass

    INSTANCE_REGISTRY._inspectors = []  # noqa: SLF001
    CLASS_REGISTRY._inspectors = []  # noqa: SLF001

    obj = MyType()
    assert get_renderer(obj, INSTANCE_HOOKS) is None
    assert get_renderer(obj, CLASS_HOOKS) is None
