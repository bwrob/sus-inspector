"""Tests for built-in inspectors."""

from __future__ import annotations

import math

from rich.console import Group
from rich.panel import Panel
from rich.table import Table

from sus_inspector.hooks.inspector import INSTANCE_REGISTRY
from sus_inspector.hooks.registry import ensure_default_hooks


def test_default_primitive_hooks() -> None:
    """Test that primitives are handled by PrimitiveInspector."""
    INSTANCE_REGISTRY._inspectors = []  # noqa: SLF001
    ensure_default_hooks()

    for val in [10, math.pi, "hello", True, None]:
        inspector = INSTANCE_REGISTRY.get_inspector(val)
        assert inspector is not None
        result = inspector(val)
        assert isinstance(result, Panel)
        assert "Primitive:" in str(result.title)


def test_default_collection_hooks() -> None:
    """Test that collections are handled by CollectionInspector."""
    INSTANCE_REGISTRY._inspectors = []  # noqa: SLF001
    ensure_default_hooks()

    # List
    val_list = [1, 2, 3]
    inspector = INSTANCE_REGISTRY.get_inspector(val_list)
    assert inspector is not None
    result = inspector(val_list)
    assert isinstance(result, Table)
    assert "List" in str(result.title)

    # Dict
    val_dict = {"a": 1}
    inspector = INSTANCE_REGISTRY.get_inspector(val_dict)
    assert inspector is not None
    result = inspector(val_dict)
    assert isinstance(result, Table)
    assert "Dict" in str(result.title)

    # Tuple
    val_tuple = (1, 2)
    inspector = INSTANCE_REGISTRY.get_inspector(val_tuple)
    assert inspector is not None
    result = inspector(val_tuple)
    assert isinstance(result, Table)
    assert "Tuple" in str(result.title)

    # Set
    val_set = {1, 2}
    inspector = INSTANCE_REGISTRY.get_inspector(val_set)
    assert inspector is not None
    result = inspector(val_set)
    assert isinstance(result, Table)
    assert "Set" in str(result.title)


def test_default_callable_hooks() -> None:
    """Test that callables are handled by CallableInspector."""
    INSTANCE_REGISTRY._inspectors = []  # noqa: SLF001
    ensure_default_hooks()

    def my_func(a: int, b: str = "default") -> int:
        """My docstring.

        Returns:
            int: The input a.

        """
        _ = b  # Unused
        return a

    inspector = INSTANCE_REGISTRY.get_inspector(my_func)
    assert inspector is not None
    result = inspector(my_func)

    assert isinstance(result, Group)

    # Verify content (Check if we have multiple panels)
    panels = [r for r in result.renderables if hasattr(r, "title")]
    titles = [str(p.title) for p in panels]
    subtitles = [str(p.subtitle) for p in panels]

    assert "Header Info" in subtitles
    assert "Signature" in titles
    assert "Docstring" in titles
