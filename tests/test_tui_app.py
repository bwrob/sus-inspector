"""Detailed tests for ObjectExplorerApp and its logic."""

from __future__ import annotations

import logging
from typing import Any, final
from unittest.mock import MagicMock, patch

import pytest
from rich.console import Console
from rich.text import Text
from textual.widgets import Input, Static, Tree
from typing_extensions import override

from sus_inspector.hooks.registry import INSTANCE_HOOKS, register_hook
from sus_inspector.tui.app import ObjectExplorerApp


def get_static_content(static: Static) -> str:
    """Get the rendered content of a Static widget.

    Args:
        static: The Static widget to render.

    Returns:
        str: The rendered string content.

    """
    console = Console(width=100, force_terminal=False)
    with console.capture() as capture:
        console.print(static.render())
    return capture.get()


@pytest.mark.asyncio
async def test_search_functionality() -> None:
    """Test searching for a node in the tree."""
    obj = {"target_node": "found me", "other": 123}
    app = ObjectExplorerApp(obj)
    async with app.run_test() as pilot:
        # Trigger search action
        await pilot.press("/")
        search_bar = app.query_one("#search-bar", Input)
        assert search_bar.display is True

        # Input search term and submit
        await pilot.press(*"target")
        await pilot.press("enter")

        # Search bar should be hidden and tree node selected
        assert search_bar.display is False
        tree = app.query_one(Tree[object])
        node = tree.cursor_node
        assert node is not None
        assert "target_node" in str(node.label)


@pytest.mark.asyncio
async def test_search_not_found() -> None:
    """Test searching for a non-existent node."""
    obj = {"a": 1}
    app = ObjectExplorerApp(obj)
    async with app.run_test() as pilot:
        await pilot.press("/")
        await pilot.press(*"missing")
        await pilot.press("enter")

        # Should just hide the search bar
        search_bar = app.query_one("#search-bar", Input)
        assert search_bar.display is False


def test_is_expandable() -> None:
    """Test the _is_expandable logic for different types."""
    app = ObjectExplorerApp({})

    # Collections
    assert app._is_expandable({"a": 1}) is True  # noqa: SLF001
    assert app._is_expandable({}) is False  # noqa: SLF001
    assert app._is_expandable([1]) is True  # noqa: SLF001
    assert app._is_expandable([]) is False  # noqa: SLF001

    # Objects with __dict__ or __slots__
    @final
    class DictObj:
        x: int

        def __init__(self) -> None:
            self.x = 1

    @final
    class SlotObj:
        __slots__: tuple[str, ...] = ("y",)
        y: int

        def __init__(self) -> None:
            self.y = 2

    assert app._is_expandable(DictObj()) is True  # noqa: SLF001
    assert app._is_expandable(SlotObj()) is True  # noqa: SLF001
    assert app._is_expandable(123) is False  # noqa: SLF001


@pytest.mark.asyncio
async def test_add_object_attributes_error_handling() -> None:
    """Test that attribute errors are handled during tree population."""

    class BrokenObj:
        @property
        def broken(self) -> Any:  # noqa: ANN401
            msg = "Prop error"
            raise ValueError(msg)

    app = ObjectExplorerApp(BrokenObj())
    async with app.run_test():
        tree = app.query_one(Tree[object])
        # The broken property should just be skipped, no crash
        labels = [str(n.label) for n in tree.root.children]
        assert "broken" not in labels


def test_add_object_attributes_generic_exception(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that generic exceptions in getattr are caught and logged."""

    class Normal:
        @override
        def __dir__(self) -> list[str]:
            return ["prop"]

    obj = Normal()

    app = ObjectExplorerApp(obj)
    mock_node = MagicMock()

    # Use a side_effect that raises for our specific attribute
    def side_effect(_o: Any, name: str) -> Any:  # noqa: ANN401
        if name == "prop":
            msg = "Generic error"
            raise RuntimeError(msg)
        raise AttributeError

    with (
        patch("sus_inspector.tui.app.getattr", side_effect=side_effect),
        caplog.at_level(logging.ERROR),
    ):
        app._add_object_attributes(mock_node, obj)  # noqa: SLF001
        assert any(
            "Failed to get attribute" in record.message for record in caplog.records
        )


@pytest.mark.asyncio
async def test_path_bar_multi_segments() -> None:
    """Test that the path bar updates correctly for nested objects."""
    obj = {"a": {"b": [10, 20]}}
    app = ObjectExplorerApp(obj)
    async with app.run_test() as pilot:
        # Expand 'a'
        await pilot.press("right")
        await pilot.wait_for_animation()
        # Down to 'a'
        await pilot.press("down")
        # Expand 'a' (the dict)
        await pilot.press("right")
        await pilot.wait_for_animation()
        # Down to 'b'
        await pilot.press("down")
        # Expand 'b'
        await pilot.press("right")
        await pilot.wait_for_animation()
        # Down to '[0]'
        await pilot.press("down")

        path_bar = app.query_one("#path-bar", Static)
        content = get_static_content(path_bar)
        assert "root.a.b" in content


@pytest.mark.asyncio
async def test_highlight_with_class_pane_visible() -> None:
    """Test highlighting a node while the class pane is visible."""
    obj = {"a": 1}
    app = ObjectExplorerApp(obj)
    async with app.run_test() as pilot:
        await pilot.press("c")  # Show class pane
        await pilot.press("down")  # Highlight 'a'
        # This covers the line: if class_pane.is_pane_visible:


@pytest.mark.asyncio
async def test_try_view_hooks_error_handling(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that failing view hooks are handled gracefully."""

    class TestObj:
        pass

    def broken_renderer(_obj: Any) -> Text:  # noqa: ANN401
        msg = "Render error"
        raise ValueError(msg)

    INSTANCE_HOOKS.clear()
    register_hook(TestObj, broken_renderer)

    app = ObjectExplorerApp(TestObj())
    with caplog.at_level(logging.ERROR):
        async with app.run_test():
            # The app should start and try to render TestObj, which will fail and log.
            assert any("View hook" in record.message for record in caplog.records)


@pytest.mark.asyncio
async def test_tree_node_none_highlight() -> None:
    """Test highlighting a node with None data."""
    obj = {"n": None}
    app = ObjectExplorerApp(obj)
    async with app.run_test() as pilot:
        await pilot.press("down")  # Highlight 'n'
        detail_view = app.query_one("#detail-view", Static)
        assert "No data." in get_static_content(detail_view)


@pytest.mark.asyncio
async def test_view_hook_callable_checker() -> None:
    """Test view hooks with a callable checker in the TUI."""

    class Special:
        pass

    def checker(obj: Any) -> bool:  # noqa: ANN401
        return isinstance(obj, Special)

    def renderer(_obj: Any) -> Text:  # noqa: ANN401
        return Text("Special View")

    INSTANCE_HOOKS.clear()
    register_hook(checker, renderer)

    app = ObjectExplorerApp(Special())
    async with app.run_test():
        detail_view = app.query_one("#detail-view", Static)
        assert "Special View" in get_static_content(detail_view)
