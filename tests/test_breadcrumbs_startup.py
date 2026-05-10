"""Test breadcrumbs on startup."""

import pytest
from textual.widgets import Button
from sus_inspector.tui.app import ObjectExplorerApp
from sus_inspector.tui.widgets import Breadcrumbs


@pytest.mark.asyncio
async def test_breadcrumbs_on_start() -> None:
    """Verify that breadcrumbs show the root on startup."""
    obj = {"a": 1}
    app = ObjectExplorerApp(obj, obj_name="ROOT")

    async with app.run_test() as pilot:
        await pilot.pause()
        breadcrumbs = app.query_one(Breadcrumbs)
        buttons = list(breadcrumbs.query(Button))
        assert len(buttons) >= 1
        assert "ROOT" in str(buttons[0].label)
