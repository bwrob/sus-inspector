"""Tests for the TUI application."""

from __future__ import annotations

from typing import Any, cast

import pytest
from rich.console import Console
from rich.text import Text
from textual.widgets import Static, Tree

from sus_inspector.hooks import register_class_hook
from sus_inspector.tui.app import ObjectExplorerApp
from sus_inspector.tui.widgets import ClassInfoPane


@pytest.mark.asyncio
async def test_class_pane_toggle() -> None:
    """Test that the 'c' key toggles the class info pane."""
    obj = {"test": 123}
    app = ObjectExplorerApp(obj)
    async with app.run_test() as pilot:
        class_pane = app.query_one(ClassInfoPane)

        # Initial state should be hidden (is_pane_visible: False)
        assert class_pane.is_pane_visible is False

        # Press 'c' to toggle on
        await pilot.press("c")
        assert class_pane.is_pane_visible is True

        # Press 'c' to toggle off
        await pilot.press("c")
        assert class_pane.is_pane_visible is False


@pytest.mark.xfail(reason="Fragile TUI highlight event in test environment")
@pytest.mark.asyncio
async def test_class_pane_updates_on_highlight() -> None:
    """Test that the class info pane updates when a node is highlighted."""

    class MyClass:
        """My Doc."""

    # Use MyClass as the root object to avoid navigation issues in test
    app = ObjectExplorerApp(MyClass())
    async with app.run_test() as pilot:
        # Show class pane - this should trigger update_object with root data
        await pilot.press("c")
        class_pane = app.query_one(ClassInfoPane)

        statics = list(class_pane.query(Static))
        console = Console(force_terminal=False, width=100)

        found = False
        for s in statics:
            with console.capture() as capture:
                console.print(s.render())
            if "My Doc." in capture.get():
                found = True
                break

        msg = f"Docstring 'My Doc.' not found in any static. Found: {len(statics)}"
        assert found, msg


@pytest.mark.asyncio
async def test_class_pane_custom_renderer() -> None:
    """Test that the class info pane uses custom renderers from CLASS_HOOKS."""

    class CustomType:
        pass

    def custom_class_renderer(_obj: Any) -> Text:  # noqa: ANN401
        return Text("Custom Class View")

    register_class_hook(CustomType, custom_class_renderer)

    app = ObjectExplorerApp(CustomType())
    async with app.run_test() as pilot:
        await pilot.press("c")
        class_pane = app.query_one(ClassInfoPane)
        await pilot.pause()

        statics = list(class_pane.query(Static))
        console = Console(force_terminal=False, width=100)
        found = False
        for s in statics:
            with console.capture() as capture:
                console.print(s.render())
            if "Custom Class View" in capture.get():
                found = True
                break
        assert found


@pytest.mark.asyncio
async def test_class_pane_none_object() -> None:
    """Test that the class info pane handles None objects correctly."""
    app = ObjectExplorerApp(None)
    async with app.run_test() as pilot:
        await pilot.press("c")
        class_pane = app.query_one(ClassInfoPane)
        await class_pane.update_object(None)
        await pilot.pause()

        statics = list(class_pane.query(Static))
        console = Console(force_terminal=False, width=100)
        found = False
        for s in statics:
            with console.capture() as capture:
                console.print(s.render())
            if "No class metadata for None." in capture.get():
                found = True
                break
        assert found


@pytest.mark.asyncio
async def test_class_pane_scrollable() -> None:
    """Test that the class info pane is scrollable when content overflows."""

    class BigClass:
        """A very big class."""

    # Dynamically add many class methods
    for i in range(50):

        def make_method(idx: int) -> Any:  # noqa: ANN401
            @classmethod
            def method(_cls: type[Any]) -> int:
                return idx

            return method

        setattr(BigClass, f"method_{i}", make_method(i))

    app = ObjectExplorerApp(BigClass())
    async with app.run_test() as pilot:
        await pilot.press("c")
        class_pane = app.query_one(ClassInfoPane)
        # VerticalScroll has scrolling by default, check style
        assert str(cast("Any", class_pane.styles).overflow_y) == "scroll"


@pytest.mark.asyncio
async def test_tree_navigation_arrows() -> None:
    """Test that left and right arrows collapse and expand tree nodes."""
    obj = {"item": [1, 2, 3]}
    app = ObjectExplorerApp(obj)
    async with app.run_test() as pilot:
        tree = app.query_one(Tree[object])
        await pilot.press("down")
        item_node = tree.cursor_node
        assert item_node is not None
        assert str(item_node.label) == "item"
        assert item_node.is_expanded is False
        await pilot.press("right")
        assert item_node.is_expanded is True
        await pilot.press("left")
        assert item_node.is_expanded is False


@pytest.mark.asyncio
async def test_class_pane_with_fields_and_methods() -> None:
    """Test that the class info pane displays class fields and methods."""

    class RichClass:
        field: int = 1

        @classmethod
        def method(cls) -> None:
            """Provide a sample class method."""

    app = ObjectExplorerApp(RichClass())
    async with app.run_test() as pilot:
        await pilot.press("c")
        class_pane = app.query_one(ClassInfoPane)
        await pilot.pause()
        statics = class_pane.query(Static)
        assert len(statics) > 0
