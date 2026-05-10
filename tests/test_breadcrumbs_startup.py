"""Test breadcrumbs on startup."""

from typing import cast

import pytest
from textual.widgets import Button, Tree

from sus_inspector.tui.app import ObjectExplorerApp
from sus_inspector.tui.widgets import Breadcrumbs


@pytest.mark.asyncio
async def test_breadcrumbs_on_start() -> None:
    """Verify that breadcrumbs show the root on startup and update on navigation."""
    obj = {"a": {"b": 1}}
    app = ObjectExplorerApp(obj, obj_name="ROOT")

    async with app.run_test() as pilot:
        await pilot.pause()
        breadcrumbs = app.query_one(Breadcrumbs)

        # Initial check
        buttons = list(breadcrumbs.query(Button))
        assert len(buttons) == 1
        assert "ROOT" in str(buttons[0].label)

        # Navigate to "a"
        tree = cast("Tree[object]", app.query_one(Tree))
        node_a = None
        for child in tree.root.children:
            if "a" in str(child.label):
                node_a = child
                break
        assert node_a is not None
        _ = tree.select_node(node_a)
        await pilot.pause()

        # Check update
        buttons = list(breadcrumbs.query(Button))
        expected_buttons = 2
        assert len(buttons) == expected_buttons
        assert "a" in str(buttons[1].label).lower()
