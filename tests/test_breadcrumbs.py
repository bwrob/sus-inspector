"""Tests for breadcrumb navigation."""

from typing import cast

import pytest
from textual.widgets import Tree

from sus_inspector.tui.app import ObjectExplorerApp
from sus_inspector.tui.widgets import Breadcrumbs


@pytest.mark.asyncio
async def test_breadcrumb_navigation() -> None:
    """Verify breadcrumb navigation functionality."""
    obj = {"a": {"b": 1}}
    app = ObjectExplorerApp(obj)

    async with app.run_test() as pilot:
        tree = cast("Tree[object]", app.query_one(Tree))
        breadcrumbs = app.query_one(Breadcrumbs)

        await pilot.pause()

        # Select "a"
        node_a = None
        for child in tree.root.children:
            if "a" in str(child.label):
                node_a = child
                break

        assert node_a is not None
        _ = tree.select_node(node_a)
        await pilot.pause()
        assert tree.cursor_node == node_a

        # Breadcrumbs should have "root" and "a"
        content = str(breadcrumbs.render())
        assert "root" in content.lower()
        assert "a" in content.lower()
