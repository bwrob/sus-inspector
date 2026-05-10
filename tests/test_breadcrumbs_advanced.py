"""Advanced tests for breadcrumbs and history interaction."""

import pytest
from textual.widgets import Tree
from sus_inspector.tui.app import ObjectExplorerApp


@pytest.mark.asyncio
async def test_history_cleared_on_toggle_private() -> None:
    """Verify that history is cleared when private members are toggled."""
    obj = {"a": 1}
    app = ObjectExplorerApp(obj)

    async with app.run_test() as pilot:
        tree = app.query_one(Tree)

        # Select "a" to add to history
        node_a = None
        for child in tree.root.children:
            if "a" in str(child.label):
                node_a = child
                break

        assert node_a is not None
        tree.select_node(node_a)
        await pilot.pause()

        assert len(app.history) > 0
        assert app.history_index >= 0

        # Toggle private
        await pilot.press("d")
        await pilot.pause()

        # History should be cleared
        assert len(app.history) == 0
        assert app.history_index == -1


@pytest.mark.asyncio
async def test_breadcrumb_none_and_handler() -> None:
    """Verify breadcrumbs with None and specialized handlers."""
    from dataclasses import dataclass

    @dataclass
    class MyData:
        x: int = 1

    obj = {"a": None, "b": MyData()}
    app = ObjectExplorerApp(obj)

    async with app.run_test() as pilot:
        tree = app.query_one(Tree)

        # Select "a" (None)
        node_a = None
        for child in tree.root.children:
            if "a" in str(child.label):
                node_a = child
                break
        assert node_a is not None
        tree.select_node(node_a)
        await pilot.pause()

        # Check detail view for None
        from textual.widgets import Static

        detail_view = app.query_one("#detail-view", Static)
        assert "No data" in str(detail_view.render())

        # Select "b" (Dataclass)
        node_b = None
        for child in tree.root.children:
            if "b" in str(child.label):
                node_b = child
                break
        assert node_b is not None
        tree.select_node(node_b)
        await pilot.pause()

        # Check handler was used (should show fields)
        assert "x" in str(detail_view.render())


@pytest.mark.asyncio
async def test_class_pane_updates_on_highlight() -> None:
    """Verify that class pane updates when a node is highlighted."""
    from textual.widgets import Static

    obj = {"a": 1}
    app = ObjectExplorerApp(obj)

    async with app.run_test() as pilot:
        # Show class pane
        await pilot.press("c")
        await pilot.pause()

        from sus_inspector.tui.widgets import ClassInfoPane

        class_pane = app.query_one(ClassInfoPane)
        assert class_pane.display is True

        # Select "a"
        tree = app.query_one(Tree)
        node_a = None
        for child in tree.root.children:
            if "a" in str(child.label):
                node_a = child
                break

        assert node_a is not None
        tree.select_node(node_a)
        await pilot.pause()

        # Class pane should have been updated and mounted something
        assert len(class_pane.query(Static)) > 0


@pytest.mark.asyncio
async def test_breadcrumb_root_name_custom() -> None:
    """Verify that breadcrumbs and history use the custom root name."""
    obj = {"a": 1}
    app = ObjectExplorerApp(obj, obj_name="CustomRoot")

    async with app.run_test() as pilot:
        # Check breadcrumbs
        from sus_inspector.tui.widgets import Breadcrumbs

        breadcrumbs = app.query_one(Breadcrumbs)
        from textual.widgets import Button

        buttons = breadcrumbs.query(Button)
        assert "CustomRoot" in str(buttons[0].label)

        # Check history modal
        await pilot.press("ctrl+h")
        await pilot.pause()

        from sus_inspector.tui.widgets import HistoryModal

        modal = app.screen
        assert isinstance(modal, HistoryModal)
        assert modal.root_name == "CustomRoot"

        # Check path string in modal
        from textual.widgets import OptionList

        option_list = modal.query_one(OptionList)
        assert "CustomRoot" in str(option_list.get_option_at_index(0).prompt)

        await pilot.press("escape")
        await pilot.pause()
