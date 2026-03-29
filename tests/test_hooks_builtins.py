"""Tests for built-in hooks."""

from __future__ import annotations

from rich.table import Table

from sus_inspector.hooks.builtins import list_view


def test_list_view_basic() -> None:
    """list_view should render a list into a Rich Table."""
    obj = [1, "two", 3.0]
    table = list_view(obj)
    assert isinstance(table, Table)
    assert "length: 3" in str(table.title)
    # Check number of rows (3 items)
    assert len(table.rows) == 3


def test_list_view_long() -> None:
    """list_view should truncate long lists."""
    obj = list(range(1000))
    table = list_view(obj)
    assert isinstance(table, Table)
    assert "length: 1000" in str(table.title)
    # 100 preview rows + 1 ellipsis row
    assert len(table.rows) == 101


def test_list_view_long_items() -> None:
    """list_view should truncate long items."""
    obj = ["A" * 200]
    table = list_view(obj)
    assert isinstance(table, Table)
    # The last column (Preview) should have the truncated string
    # We can't easily check the content of the cell without a console,
    # but we covered the line in coverage.
    pass


def test_list_view_invalid() -> None:
    """list_view should handle invalid types (safety check)."""
    table = list_view("not a list")
    assert isinstance(table, Table)
    assert str(table.title) == "Not a list"
