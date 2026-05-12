"""Tests for history modal search."""

from typing import cast

import pytest
from textual.widgets import OptionList, Tree

from sus_inspector.tui.app import ObjectExplorerApp


@pytest.mark.asyncio
async def test_history_modal_search() -> None:
    """Verify history modal search functionality."""
    obj = {"apple": 1, "banana": 2}
    app = ObjectExplorerApp(obj)

    async with app.run_test() as pilot:
        tree = cast("Tree[object]", app.query_one(Tree))

        await pilot.pause()

        # Select "apple"
        node_apple = None
        for child in tree.root.children:
            if "apple" in str(child.label):
                node_apple = child
                break
        _ = tree.select_node(node_apple)
        await pilot.pause()

        # Select "banana"
        node_banana = None
        for child in tree.root.children:
            if "banana" in str(child.label):
                node_banana = child
                break
        _ = tree.select_node(node_banana)
        await pilot.pause()

        # Show history
        await pilot.press("ctrl+h")
        await pilot.pause()

        # Type "app" in search
        await pilot.press("a", "p", "p")
        await pilot.pause()

        option_list = app.screen.query_one(OptionList)
        assert option_list.option_count == 1
        assert "apple" in str(option_list.get_option_at_index(0).prompt).lower()

        # Select it
        await pilot.press("enter")
        await pilot.pause()

        assert tree.cursor_node == node_apple
