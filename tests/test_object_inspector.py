"""Tests for ObjectInspector."""

from __future__ import annotations

from typing import Any

from rich.console import Group
from rich.table import Table

from sus_inspector.hooks.builtins import ObjectInspector


class MockObject:
    """Mock object for testing ObjectInspector."""

    attr1: str
    _private: str

    def __init__(self) -> None:
        """Initialize mock object."""
        self.attr1 = "value1"
        self._private = "secret"

    @staticmethod
    def method1() -> bool:
        """Return True for testing.

        Returns:
            bool: Always True.

        """
        return True


def test_object_inspector() -> None:
    """Test that ObjectInspector identifies public members and returns a Group."""
    obj = MockObject()
    inspector = ObjectInspector()
    result = inspector(obj)

    assert isinstance(result, Group)

    # Check for sections
    tables = [r for r in result.renderables if isinstance(r, Table)]
    titles = [str(t.title) for t in tables]

    assert "Attributes" in titles
    assert "Methods" in titles

    # Verify content in tables
    all_cells: list[Any] = []
    for table in tables:
        for col in table.columns:
            # Column._cells is private but necessary for testing content
            all_cells.extend([str(cell) for cell in col._cells])  # noqa: SLF001

    assert "attr1" in all_cells
    assert "method1" in all_cells
    assert "__doc__" not in all_cells
    assert "_private" not in all_cells
