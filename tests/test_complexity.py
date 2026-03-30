"""Tests for complexity assessment."""

from __future__ import annotations

from typing import Final

from sus_inspector.hooks.complexity import get_object_complexity, is_complex_object

FIELD_COUNT_2: Final = 2
DEPTH_1: Final = 1
SIZE_3: Final = 3
DEPTH_3: Final = 3
DEPTH_THRESHOLD_2: Final = 2


class Simple:
    """Simple object."""

    a: int
    b: int

    def __init__(self) -> None:
        """Initialize."""
        self.a = 1
        self.b = 2


class Complex:
    """Complex nested object."""

    child: Complex | None
    data: list[int]

    def __init__(self, depth: int) -> None:
        """Initialize."""
        if depth > 0:
            self.child = Complex(depth - 1)
        else:
            self.child = None
        self.data = list(range(10))


def test_get_object_complexity() -> None:
    """Test get_object_complexity function."""
    simple = Simple()
    metrics = get_object_complexity(simple)
    assert metrics["field_count"] == FIELD_COUNT_2
    assert metrics["depth"] == DEPTH_1
    assert metrics["total_size"] == SIZE_3  # self + a + b

    nested = Complex(2)
    metrics = get_object_complexity(nested, max_depth=5)
    assert metrics["field_count"] == FIELD_COUNT_2  # child, data
    assert metrics["depth"] == DEPTH_3  # self -> child -> child -> child(None)


def test_is_complex_object() -> None:
    """Test is_complex_object function."""
    simple = Simple()
    assert is_complex_object(simple) is False

    # Field count threshold
    class ManyFields:
        """Object with many fields."""

        def __init__(self) -> None:
            """Initialize."""
            for i in range(15):
                setattr(self, f"f{i}", i)

    assert is_complex_object(ManyFields()) is True

    # Depth threshold
    nested = Complex(5)
    assert is_complex_object(nested, depth_threshold=DEPTH_THRESHOLD_2) is True
