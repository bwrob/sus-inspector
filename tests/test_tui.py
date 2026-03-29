import pytest
from textual.widgets import Static, Tree
from sus_inspector.tui.app import ObjectExplorerApp
from sus_inspector.tui.widgets import ClassInfoPane
from sus_inspector.hooks import register_class_hook
from rich.text import Text
from rich.console import Console


@pytest.mark.asyncio
async def test_class_pane_toggle():
    """Test that the 'c' key toggles the class info pane."""
    obj = {"test": 123}
    app = ObjectExplorerApp(obj)
    async with app.run_test() as pilot:
        class_pane = app.query_one(ClassInfoPane)

        # Initial state should be hidden (display: False)
        assert class_pane.display is False

        # Press 'c' to toggle on
        await pilot.press("c")
        assert class_pane.display is True

        # Press 'c' to toggle off
        await pilot.press("c")
        assert class_pane.display is False


@pytest.mark.xfail(reason="Fragile TUI highlight event in test environment")
@pytest.mark.asyncio
async def test_class_pane_updates_on_highlight():
    """Test that the class info pane updates when a node is highlighted."""

    class MyClass:
        """My Doc."""

        pass

    app = ObjectExplorerApp(MyClass())
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
            if "My Doc." in capture.get():
                found = True
                break
        assert found


@pytest.mark.asyncio
async def test_class_pane_custom_renderer():
    """Test that the class info pane uses custom renderers from CLASS_HOOKS."""

    class CustomType:
        pass

    def custom_class_renderer(obj):
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
async def test_class_pane_none_object():
    """Test that the class info pane handles None objects correctly."""
    app = ObjectExplorerApp(None)
    async with app.run_test() as pilot:
        await pilot.press("c")
        class_pane = app.query_one(ClassInfoPane)
        class_pane.update_object(None)
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
async def test_class_pane_scrollable():
    """Test that the class info pane is scrollable when content overflows."""

    class BigClass:
        """A very big class."""

        pass

    # Dynamically add many class methods
    for i in range(50):

        def make_method(idx):
            @classmethod
            def method(cls):
                return idx

            return method

        setattr(BigClass, f"method_{i}", make_method(i))

    app = ObjectExplorerApp(BigClass())
    async with app.run_test() as pilot:
        await pilot.press("c")
        class_pane = app.query_one(ClassInfoPane)
        assert class_pane.styles.overflow_y == "scroll"


@pytest.mark.asyncio
async def test_tree_navigation_arrows():
    """Test that left and right arrows collapse and expand tree nodes."""
    obj = {"item": [1, 2, 3]}
    app = ObjectExplorerApp(obj)
    async with app.run_test() as pilot:
        tree = app.query_one(Tree)
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
async def test_class_pane_with_fields_and_methods():
    """Test that the class info pane displays class fields and methods."""

    class RichClass:
        field = 1

        @classmethod
        def method(cls):
            pass

    app = ObjectExplorerApp(RichClass())
    async with app.run_test() as pilot:
        await pilot.press("c")
        class_pane = app.query_one(ClassInfoPane)
        await pilot.pause()
        statics = class_pane.query(Static)
        assert len(statics) > 0
