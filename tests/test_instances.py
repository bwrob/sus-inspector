"""Tests for global instances."""

from __future__ import annotations

from sus_inspector.core import InteractiveExplorer
from sus_inspector.instances import sus


def test_sus_instance() -> None:
    """The global sus instance should be an InteractiveExplorer."""
    assert isinstance(sus, InteractiveExplorer)
