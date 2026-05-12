"""Tests for history navigation logic."""

from typing import cast

import pytest
from textual.widgets import Tree

from sus_inspector.tui.app import ObjectExplorerApp


@pytest.mark.asyncio
async def test_history_navigation_logic() -> None:
    """Verify history navigation logic."""
    obj = {"a": {"b": 1}, "c": 2}
    app = ObjectExplorerApp(obj)

    async with app.run_test() as pilot:
        tree = cast("Tree[object]", app.query_one(Tree))

        # Initial state: root selected (usually on_mount selects root)
        # Wait for tree to be populated
        await pilot.pause()

        # root is at index 0
        assert len(app.history) == 1
        assert app.history[0] == tree.root
        assert app.history_index == 0

        # Select "a"
        # We need to find the node for "a"
        node_a = None
        for child in tree.root.children:
            if "a" in str(child.label):
                node_a = child
                break

        assert node_a is not None
        _ = tree.select_node(node_a)
        await pilot.pause()

        expected_len = 2
        assert len(app.history) == expected_len
        assert app.history[1] == node_a
        assert app.history_index == 1
        # Go back
        await pilot.press("alt+left")
        await pilot.pause()
        await pilot.pause()
        assert app.history_index == 0
        assert tree.cursor_node == tree.root

        # Go forward
        await pilot.press("alt+right")
        await pilot.pause()
        await pilot.pause()
        assert app.history_index == 1
        assert tree.cursor_node is not None
        assert tree.cursor_node.data == obj["a"]
