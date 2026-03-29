"""Property-based tests for metadata extraction."""

from __future__ import annotations

from hypothesis import given, strategies as st
from sus_inspector.metadata import get_class_metadata


@given(st.from_type(object))
def test_get_class_metadata_robustness(obj: object) -> None:
    """get_class_metadata should not crash for any object type."""
    metadata = get_class_metadata(obj)
    assert isinstance(metadata.name, str)
    assert isinstance(metadata.mro, list)
    assert all(isinstance(m, str) for m in metadata.mro)
