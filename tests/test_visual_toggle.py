"""Tests for visual toggle and smart grouping."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
from textual.widgets import Tree

from sus_inspector.tui.app import ObjectExplorerApp

if TYPE_CHECKING:
    from textual.widgets.tree import TreeNode


class LargeObject:
    """An object with many members to trigger smart grouping."""

    def __init__(self) -> None:
        self.f1 = 1
        self.f2 = 2
        self.f3 = 3
        self.f4 = 4
        self.f5 = 5
        self.f6 = 6

    def m1(self) -> None: pass
    def m2(self) -> None: pass
    def m3(self) -> None: pass
    def m4(self) -> None: pass
    def m5(self) -> None: pass


@pytest.mark.asyncio
async def test_show_private_toggle_state() -> None:
    """Test that the 'd' key toggles show_private state."""
    app = ObjectExplorerApp({})
    async with app.run_test() as pilot:
        assert app.show_private is False
        await pilot.press("d")
        assert app.show_private is True
        await pilot.press("d")
        assert app.show_private is False


@pytest.mark.asyncio
async def test_smart_grouping_threshold() -> None:
    """Test that objects with many members are grouped."""
    obj = LargeObject()
    # 6 fields + 5 methods = 11 members (over threshold 10)
    app = ObjectExplorerApp(obj)
    async with app.run_test():
        tree = app.query_one(Tree[object])
        root_children = tree.root.children
        
        # Should have "Fields (6)" and "Methods (5)" virtual nodes
        labels = [str(n.label) for n in root_children]
        assert any("Fields" in l for l in labels)
        assert any("Methods" in l for l in labels)
        
        # Verify specific counts in labels if possible
        fields_node = next(n for n in root_children if "Fields" in str(n.label))
        methods_node = next(n for n in root_children if "Methods" in str(n.label))
        
        assert "(6)" in str(fields_node.label)
        assert "(5)" in str(methods_node.label)


@pytest.mark.asyncio
async def test_small_object_no_grouping() -> None:
    """Test that small objects are not grouped."""
    class SmallObject:
        def __init__(self) -> None:
            self.a = 1
            self.b = 2
    
    app = ObjectExplorerApp(SmallObject())
    async with app.run_test():
        tree = app.query_one(Tree[object])
        root_children = tree.root.children
        labels = [str(n.label) for n in root_children]
        
        assert not any("Fields" in l for l in labels)
        assert "a" in labels
        assert "b" in labels


@pytest.mark.asyncio
async def test_private_member_visibility() -> None:
    """Test that private members are hidden/shown correctly."""
    class PrivateObj:
        def __init__(self) -> None:
            self.public = 1
            self._private = 2
    
    app = ObjectExplorerApp(PrivateObj())
    async with app.run_test() as pilot:
        tree = app.query_one(Tree[object])
        
        # Initially hidden
        assert not any("_private" in str(n.label) for n in tree.root.children)
        assert any("public" in str(n.label) for n in tree.root.children)
        
        # Toggle 'd'
        await pilot.press("d")
        
        # Now shown
        assert any("_private" in str(n.label) for n in tree.root.children)
