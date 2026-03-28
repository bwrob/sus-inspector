"""Tests for the core InteractiveExplorer logic."""

from __future__ import annotations

from unittest.mock import patch

from sus_inspector.core import InteractiveExplorer


def test_explorer_call_returns_object() -> None:
    """The explorer should return the object it inspects and call _run."""
    explorer = InteractiveExplorer()
    obj = {"test": 123}

    with patch.object(InteractiveExplorer, "_run") as mock_run:
        result = explorer(obj, name="my_obj")
        assert result is obj
        mock_run.assert_called_once_with(obj, "my_obj")


def test_explorer_truediv_returns_object() -> None:
    """The explorer should return the object it inspects when using '/'."""
    explorer = InteractiveExplorer()
    obj = [1, 2, 3]

    with patch.object(InteractiveExplorer, "_run") as mock_run:
        result = explorer / obj
        assert result is obj
        mock_run.assert_called_once_with(obj, "list")
