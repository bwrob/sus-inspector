"""Tests for TUI paging and expansion logic."""

from __future__ import annotations

import dataclasses

import pytest
from textual.widgets import Tree

from sus_inspector.tui.app import MAX_TREE_CHILDREN, ObjectExplorerApp


@pytest.mark.asyncio
async def test_tui_paging_dict() -> None:
    """Test that large dicts are paged in the tree."""
    large_dict = {f"k{i}": i for i in range(MAX_TREE_CHILDREN + 10)}
    app = ObjectExplorerApp(large_dict)

    async with app.run_test() as pilot:
        tree = app.query_one(Tree[object])
        # Root is expanded by default in on_mount
        # Wait for children to be added
        await pilot.pause()

        # Should have MAX_TREE_CHILDREN nodes + 1 "more" node
        assert len(tree.root.children) == MAX_TREE_CHILDREN + 1
        assert "more" in str(tree.root.children[-1].label)


@pytest.mark.asyncio
async def test_tui_paging_list() -> None:
    """Test that large lists are paged in the tree."""
    large_list = list(range(MAX_TREE_CHILDREN + 10))
    app = ObjectExplorerApp(large_list)

    async with app.run_test() as pilot:
        tree = app.query_one(Tree[object])
        await pilot.pause()

        assert len(tree.root.children) == MAX_TREE_CHILDREN + 1
        assert "more" in str(tree.root.children[-1].label)


@pytest.mark.asyncio
async def test_tui_expansion_toggle() -> None:
    """Test the 'e' key binding to toggle expansion."""

    @dataclasses.dataclass
    class Large:
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

    obj = Large()
    app = ObjectExplorerApp(obj)

    async with app.run_test() as pilot:
        await pilot.pause()

        # Initially summary (complex object)
        obj_id = id(obj)
        assert obj_id not in app.expanded_details

        # Press 'e'
        await pilot.press("e")
        await pilot.pause()

        # Now expanded
        assert obj_id in app.expanded_details

        # Press 'e' again
        await pilot.press("e")
        await pilot.pause()
        assert obj_id not in app.expanded_details
