"""Tests for the hook registry system."""

from __future__ import annotations

from typing import Any
from unittest.mock import patch

from pydantic import BaseModel
from rich.text import Text

from sus_inspector.hooks.inspector import CLASS_REGISTRY, INSTANCE_REGISTRY
from sus_inspector.hooks.registry import (
    CLASS_HOOKS,
    INSTANCE_HOOKS,
    ensure_default_hooks,
    get_renderer,
    register_class_hook,
    register_hook,
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


def test_register_hook_alias() -> None:
    """register_hook should be an alias for register_instance_hook."""
    INSTANCE_HOOKS.clear()

    def renderer(_obj: Any) -> Text:  # noqa: ANN401
        return Text("test")

    register_hook(int, renderer)
    assert (int, renderer) in INSTANCE_HOOKS


def test_get_renderer_with_callable_checker() -> None:
    """get_renderer should support callable type checkers."""
    INSTANCE_HOOKS.clear()

    def renderer(_obj: Any) -> Text:  # noqa: ANN401
        return Text("matched")

    def checker(obj: Any) -> bool:  # noqa: ANN401
        return hasattr(obj, "special_attr")

    register_hook(checker, renderer)

    class SpecialObj:
        special_attr: bool = True

    obj = SpecialObj()
    assert get_renderer(obj, INSTANCE_HOOKS) == renderer
    assert get_renderer(123, INSTANCE_HOOKS) is None


def test_ensure_default_hooks() -> None:
    """ensure_default_hooks should populate the registry."""
    INSTANCE_HOOKS.clear()
    ensure_default_hooks()
    assert len(INSTANCE_HOOKS) >= 1
    # Check if list hook is registered
    assert get_renderer([], INSTANCE_HOOKS) is not None

    # Calling it again should do nothing
    current_len = len(INSTANCE_HOOKS)
    ensure_default_hooks()
    assert len(INSTANCE_HOOKS) == current_len


def test_ensure_default_hooks_no_pydantic() -> None:
    """ensure_default_hooks should handle missing pydantic gracefully."""
    INSTANCE_HOOKS.clear()

    # We need to simulate the ImportError during 'from pydantic import BaseModel'
    # We mock __import__ to raise ImportError specifically for pydantic
    orig_import = __import__

    def mocked_import(name: str, *args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        if name == "pydantic":
            msg = "Mocked error"
            raise ImportError(msg)
        return orig_import(name, *args, **kwargs)

    with patch("builtins.__import__", side_effect=mocked_import):
        ensure_default_hooks()
        # Should have registered list, but not pydantic
        # Assuming list_view is always registered first
        assert len(INSTANCE_HOOKS) == 1
        assert INSTANCE_HOOKS[0][0] is list

    # Restore and verify it registers both now
    INSTANCE_HOOKS.clear()
    ensure_default_hooks()
    # It should register list and BaseModel (since pydantic is available in env)
    assert any(h[0] is BaseModel for h in INSTANCE_HOOKS)
