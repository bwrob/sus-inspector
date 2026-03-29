"""Tests for ObjectInspector."""

from rich.table import Table
from sus_inspector.hooks.builtins import ObjectInspector


class MockObject:
    """Mock object for testing ObjectInspector."""

    def __init__(self):
        self.attr1 = "value1"
        self._private = "secret"

    def method1(self):
        """Method 1 docstring."""
        return True


def test_object_inspector():
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
        all_cells.extend([str(cell) for cell in col._cells])

    assert "__doc__" in all_cells
    assert "attr1" in all_cells
    assert "method1" in all_cells
    assert "_private" not in all_cells
