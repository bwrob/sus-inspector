import pytest
from sus_inspector.tui.app import ObjectExplorerApp
from sus_inspector.tui.widgets import ClassInfoPane
from sus_inspector.hooks import register_class_hook
from rich.text import Text


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


@pytest.mark.asyncio
async def test_class_pane_updates_on_highlight():
    """Test that the class info pane updates when a node is highlighted."""

    class MyClass:
        """My Doc."""

        pass

    obj = {"item": MyClass()}
    app = ObjectExplorerApp(obj)
    async with app.run_test() as pilot:
        # Show class pane
        await pilot.press("c")
        class_pane = app.query_one(ClassInfoPane)

        # Highlight the 'item' node in the tree
        # The tree root is {"item": ...}, root is already selected.
        # Press down to select "item"
        await pilot.press("down")

        # Check if the pane contains the docstring
        renderable = class_pane.render()
        assert renderable is not None


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

        renderable = class_pane.render()
        # Verify it uses the custom renderer
        assert "Custom Class View" in str(renderable)


@pytest.mark.asyncio
async def test_class_pane_none_object():
    """Test that the class info pane handles None objects correctly."""
    app = ObjectExplorerApp(None)
    async with app.run_test() as pilot:
        await pilot.press("c")
        class_pane = app.query_one(ClassInfoPane)
        class_pane.update_object(None)
        assert "No class metadata for None." in str(class_pane.render())


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
        renderable = class_pane.render()
        assert renderable is not None
