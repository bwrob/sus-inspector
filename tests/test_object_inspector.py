"""Tests for ObjectInspector."""

from __future__ import annotations

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
    """Test that ObjectInspector identifies public members."""
    obj = MockObject()
    inspector = ObjectInspector()
    result = inspector(obj)

    assert isinstance(result, Table)
    assert "Object: MockObject" in str(result.title)

    # Verify columns and rows content
    column_names = [str(col.header) for col in result.columns]
    assert "Member" in column_names

    # Check that member1 and attr1 are somewhere in the cells
    all_cells = []
    for col in result.columns:
        all_cells.extend([str(cell) for cell in col._cells])  # noqa: SLF001

    assert "attr1" in all_cells
    assert "method1" in all_cells
    assert "__doc__" not in all_cells
    assert "_private" not in all_cells
