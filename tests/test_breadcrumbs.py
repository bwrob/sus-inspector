"""Tests for breadcrumb navigation."""

import pytest
from textual.widgets import Button, Tree

from sus_inspector.tui.app import ObjectExplorerApp
from sus_inspector.tui.widgets import Breadcrumbs


@pytest.mark.asyncio
async def test_breadcrumb_navigation() -> None:
    """Verify breadcrumb navigation functionality."""
    obj = {"a": {"b": 1}}
    app = ObjectExplorerApp(obj)

    async with app.run_test() as pilot:
        tree = app.query_one(Tree)
        breadcrumbs = app.query_one(Breadcrumbs)

        await pilot.pause()

        # Select "a"
        node_a = None
        for child in tree.root.children:
            if "a" in str(child.label):
                node_a = child
                break

        assert node_a is not None
        tree.select_node(node_a)
        await pilot.pause()

        # Breadcrumbs should have "root" and "a"
        buttons = breadcrumbs.query(Button)
        expected_buttons = 2
        assert len(buttons) == expected_buttons
        assert "root" in str(buttons[0].label).lower()
        assert "a" in str(buttons[1].label).lower()

        # Press "root" button in breadcrumbs
        buttons[0].press()
        await pilot.pause()
        assert tree.cursor_node == tree.root
