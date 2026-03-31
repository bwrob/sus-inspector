"""Tests for specialized class views."""

from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, Any, Final, cast

import attr
import msgspec
import pytest
from rich.console import Console, Group
from rich.table import Table
from textual.app import App, ComposeResult
from typing_extensions import override

from sus_inspector.hooks.attrs import AttrsHandler
from sus_inspector.hooks.base import BaseObjectHandler
from sus_inspector.hooks.dataclasses import DataclassHandler
from sus_inspector.hooks.msgspec import MsgspecHandler
from sus_inspector.tui.widgets import ClassInfoPane

if TYPE_CHECKING:
    from textual.widgets import Static

FIELD_COUNT_2: Final = 2
MIN_PANE_CHILDREN: Final = 2
RENDERABLES_COUNT_2: Final = 2


def test_dataclass_field_metadata() -> None:
    """Test DataclassHandler field metadata extraction."""

    @dataclasses.dataclass
    class MyDC:
        a: int
        b: str = "default"

    handler = DataclassHandler()
    meta = handler.get_field_metadata(MyDC)
    assert len(meta) == FIELD_COUNT_2
    assert meta[0]["name"] == "a"
    assert meta[1]["name"] == "b"
    assert meta[1]["default_value"] == "default"


def test_attrs_field_metadata() -> None:
    """Test AttrsHandler field metadata extraction."""

    @attr.s
    class MyAttr:
        a: int = attr.ib()
        b: str = attr.ib(default="default", metadata={"description": "desc"})

    handler = AttrsHandler()
    meta = handler.get_field_metadata(MyAttr)
    assert len(meta) == FIELD_COUNT_2
    assert meta[0]["name"] == "a"
    assert meta[1]["name"] == "b"
    assert meta[1]["description"] == "desc"
    assert meta[1]["default_value"] == "default"


def test_msgspec_field_metadata() -> None:
    """Test MsgspecHandler field metadata extraction."""

    class MyStruct(msgspec.Struct):
        a: int
        b: str = "default"

    handler = MsgspecHandler()
    meta = handler.get_field_metadata(MyStruct)
    assert len(meta) == FIELD_COUNT_2
    assert meta[0]["name"] == "a"
    assert meta[1]["name"] == "b"
    assert meta[1]["default_value"] == "default"


def test_base_handler_render_class_view() -> None:
    """Test the base render_class_view method."""

    @dataclasses.dataclass
    class MyDC:
        field1: int

        def method1(self) -> None:
            """Doc."""

    handler = DataclassHandler()
    renderable = handler.render_class_view(MyDC)
    assert isinstance(renderable, Group)
    # Group should contain Field Schema table and Methods table
    assert len(renderable.renderables) == RENDERABLES_COUNT_2

    # Test with no metadata (Mock)
    class EmptyHandler(BaseObjectHandler):
        @override
        def can_handle(self, obj: Any) -> bool:
            return False

        @override
        def get_type_tag(self, obj: Any) -> str:
            return ""

        @override
        def get_fields(self, obj: Any) -> dict[str, Any]:
            return {}

    empty = EmptyHandler()
    assert "No field or method metadata" in str(empty.render_class_view(None))


def test_base_handler_get_methods() -> None:
    """Test get_methods extraction."""

    class MyClass:
        def m1(self) -> None:
            pass

        @classmethod
        def m2(cls) -> None:
            pass

        @staticmethod
        def m3() -> None:
            pass

    handler = DataclassHandler()
    methods = handler.get_methods(MyClass())
    assert "m1" in methods
    assert "m2" in methods
    assert "m3" in methods
    assert "__init__" not in methods


def test_base_handler_render_instance_with_methods() -> None:
    """Test instance rendering includes methods section."""

    @dataclasses.dataclass
    class MyDC:
        a: int

        def action(self) -> None:
            pass

    handler = DataclassHandler()
    renderable = handler.render(MyDC(a=1), expanded=True)

    console = Console(width=100)
    with console.capture() as capture:
        console.print(renderable)
    output = capture.get()

    assert "Methods:" in output
    assert "action()" in output


def test_render_method_table_exception() -> None:
    """Test _render_method_table with a function that has no signature."""
    handler = DataclassHandler()
    # Built-in functions often don't have a readable signature via inspect.signature
    methods = {"built_in": len}
    table = handler._render_method_table(methods)  # noqa: SLF001
    assert isinstance(table, Table)

    console = Console(width=100)
    with console.capture() as capture:
        console.print(table)
    output = capture.get()
    assert "built_in" in output


def test_render_class_view_totally_empty() -> None:
    """Test render_class_view with no fields and no methods."""

    class EmptyHandler(BaseObjectHandler):
        @override
        def can_handle(self, obj: Any) -> bool:
            return False

        @override
        def get_type_tag(self, obj: Any) -> str:
            return ""

        @override
        def get_fields(self, obj: Any) -> dict[str, Any]:
            return {}

        @override
        def get_field_metadata(self, obj: Any) -> list[Any]:
            return []

        @override
        def get_methods(self, obj: Any) -> dict[str, Any]:
            return {}

    handler = EmptyHandler()
    # Should trigger the "No field or method metadata available" branch
    renderable = handler.render_class_view(object())
    assert "No field or method metadata" in str(renderable)


@pytest.mark.asyncio
async def test_class_info_pane_specialized_handler() -> None:
    """Test ClassInfoPane uses specialized handlers."""

    @dataclasses.dataclass
    class MyDC:
        a: int

    class TestApp(App[None]):
        @override
        def compose(self) -> ComposeResult:
            yield ClassInfoPane(id="pane")

    app = TestApp()
    async with app.run_test() as pilot:
        pane = app.query_one(ClassInfoPane)
        pane.update_object(MyDC(a=1))
        await pilot.pause()

        # Verify children are mounted
        # 1. Specialized group (Field Schema + Methods)
        # 2. Base metadata (MRO/Hierarchy)
        assert len(pane.children) >= MIN_PANE_CHILDREN


@pytest.mark.asyncio
async def test_class_info_pane_fallback() -> None:
    """Test ClassInfoPane fallback to default metadata."""

    class RegularClass:
        pass

    class TestApp(App[None]):
        @override
        def compose(self) -> ComposeResult:
            yield ClassInfoPane(id="pane")

    app = TestApp()
    async with app.run_test() as pilot:
        pane = app.query_one(ClassInfoPane)
        pane.update_object(RegularClass())
        await pilot.pause()

        # Should show MRO/Hierarchy at least
        assert len(pane.children) >= 1


@pytest.mark.asyncio
async def test_class_info_pane_none() -> None:
    """Test ClassInfoPane with None."""

    class TestApp(App[None]):
        @override
        def compose(self) -> ComposeResult:
            yield ClassInfoPane(id="pane")

    app = TestApp()
    async with app.run_test() as pilot:
        pane = app.query_one(ClassInfoPane)
        pane.update_object(None)
        await pilot.pause()

        child = cast("Static", pane.children[0])
        assert "No class metadata for None" in str(child.render())
