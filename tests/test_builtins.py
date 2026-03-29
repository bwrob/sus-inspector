"""Tests for built-in inspectors."""

from rich.panel import Panel
from rich.table import Table
from sus_inspector.hooks.registry import INSTANCE_REGISTRY, ensure_default_hooks


def test_default_primitive_hooks():
    """Test that primitives are handled by PrimitiveInspector."""
    INSTANCE_REGISTRY._inspectors = []
    ensure_default_hooks()

    for val in [10, 3.14, "hello", True, None]:
        inspector = INSTANCE_REGISTRY.get_inspector(val)
        assert inspector is not None
        result = inspector(val)
        assert isinstance(result, Panel)
        assert "Primitive:" in str(result.title)


def test_default_collection_hooks():
    """Test that collections are handled by CollectionInspector."""
    INSTANCE_REGISTRY._inspectors = []
    ensure_default_hooks()

    # List
    val_list = [1, 2, 3]
    inspector = INSTANCE_REGISTRY.get_inspector(val_list)
    assert inspector is not None
    result = inspector(val_list)
    assert isinstance(result, Table)
    assert "List" in str(result.title)

    # Dict
    val_dict = {"a": 1}
    inspector = INSTANCE_REGISTRY.get_inspector(val_dict)
    assert inspector is not None
    result = inspector(val_dict)
    assert isinstance(result, Table)
    assert "Dict" in str(result.title)

    # Tuple
    val_tuple = (1, 2)
    inspector = INSTANCE_REGISTRY.get_inspector(val_tuple)
    assert inspector is not None
    result = inspector(val_tuple)
    assert isinstance(result, Table)
    assert "Tuple" in str(result.title)

    # Set
    val_set = {1, 2}
    inspector = INSTANCE_REGISTRY.get_inspector(val_set)
    assert inspector is not None
    result = inspector(val_set)
    assert isinstance(result, Table)
    assert "Set" in str(result.title)


def test_default_callable_hooks():
    """Test that callables are handled by CallableInspector."""
    INSTANCE_REGISTRY._inspectors = []
    ensure_default_hooks()

    def my_func(a: int, b: str = "default"):
        """My docstring."""
        return a

    inspector = INSTANCE_REGISTRY.get_inspector(my_func)
    assert inspector is not None
    result = inspector(my_func)
    assert isinstance(result, Table)
    assert "Callable:" in str(result.title)

    # Verify content (Signature, Docstring)
    all_cells = []
    for col in result.columns:
        all_cells.extend([str(cell) for cell in col._cells])

    assert "my_func" in all_cells
    assert "My docstring." in all_cells
    assert "(a: int, b: str = 'default')" in all_cells
