"""Tests for visual toggle and smart grouping."""

from __future__ import annotations

from typing import final

import pytest
from textual.widgets import Tree

from sus_inspector.tui.app import ObjectExplorerApp


@final
class LargeObject:
    """An object with many members to trigger smart grouping."""

    f1: int
    f2: int
    f3: int
    f4: int
    f5: int
    f6: int

    def __init__(self) -> None:
        """Initialize LargeObject."""
        self.f1 = 1
        self.f2 = 2
        self.f3 = 3
        self.f4 = 4
        self.f5 = 5
        self.f6 = 6

    def m1(self) -> None:
        """Represent Method 1."""

    def m2(self) -> None:
        """Represent Method 2."""

    def m3(self) -> None:
        """Represent Method 3."""

    def m4(self) -> None:
        """Represent Method 4."""

    def m5(self) -> None:
        """Represent Method 5."""


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
        assert any("Fields" in label for label in labels)
        assert any("Methods" in label for label in labels)

        # Verify specific counts in labels if possible
        fields_node = next(n for n in root_children if "Fields" in str(n.label))
        methods_node = next(n for n in root_children if "Methods" in str(n.label))

        assert "(6)" in str(fields_node.label)
        assert "(5)" in str(methods_node.label)


@pytest.mark.asyncio
async def test_small_object_no_grouping() -> None:
    """Test that small objects are not grouped."""

    @final
    class SmallObject:
        """Small test object."""

        a: int
        b: int

        def __init__(self) -> None:
            """Initialize SmallObject."""
            self.a = 1
            self.b = 2

    app = ObjectExplorerApp(SmallObject())
    async with app.run_test():
        tree = app.query_one(Tree[object])
        root_children = tree.root.children
        labels = [str(n.label) for n in root_children]

        assert not any("Fields" in label for label in labels)
        assert any("a" in label for label in labels)
        assert any("b" in label for label in labels)


@pytest.mark.asyncio
async def test_private_member_visibility() -> None:
    """Test that private members are hidden/shown correctly."""

    @final
    class PrivateObj:
        """Test object with private members."""

        public: int
        _private: int

        def __init__(self) -> None:
            """Initialize PrivateObj."""
            self.public = 1
            self._private = 2

    app = ObjectExplorerApp(PrivateObj())
    app.grouping_threshold = 100
    async with app.run_test() as pilot:
        tree = app.query_one(Tree[object])

        # Initially hidden
        labels_before = [str(n.label) for n in tree.root.children]
        assert not any("_private" in label for label in labels_before)
        assert any("public" in label for label in labels_before)

        # Toggle 'd'
        await pilot.press("d")
        await pilot.wait_for_animation()

        # Now shown
        labels_after = [str(n.label) for n in tree.root.children]
        assert any("_private" in label for label in labels_after)
