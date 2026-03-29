"""Tests for the class metadata extraction logic."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from sus_inspector.metadata import get_class_metadata

if TYPE_CHECKING:
    from rich.text import Text


class Base:
    """Base class doc."""

    base_field: str = "base"


class Sub(Base):
    """Sub class doc."""

    sub_field: str = "sub"

    @classmethod
    def sub_method(cls) -> None:
        """Provide a sample class method."""


def test_get_class_metadata() -> None:
    """Test extracting metadata from a class and its instance."""
    obj = Sub()
    meta = get_class_metadata(obj)

    assert meta.name == "Sub"
    assert meta.doc == "Sub class doc."
    assert "sub_field" in meta.class_fields
    assert "base_field" in meta.class_fields
    assert "sub_method" in meta.class_methods
    assert "Sub" in meta.mro
    assert "Base" in meta.mro
    assert "object" in meta.mro


def test_inheritance_tree_structure() -> None:
    """Test that the inheritance tree root is correct."""
    obj = Sub()
    meta = get_class_metadata(obj)
    # Tree visualization is hard to assert exactly,
    # but we can check if it exists and has the right root.
    label = cast("Text", meta.inheritance_tree.label)
    assert label.plain == "Sub"
