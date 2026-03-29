"""Tests for the core InteractiveExplorer logic."""

from __future__ import annotations

from unittest.mock import MagicMock, patch


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


def test_explorer_truediv_ellipsis() -> None:
    """The explorer should capture locals when using '/' with Ellipsis."""
    explorer = InteractiveExplorer()
    local_var = "hello"  # noqa: F841

    with patch.object(InteractiveExplorer, "_run") as mock_run:
        result = explorer / ...
        assert result is None
        mock_run.assert_called_once()
        args, _ = mock_run.call_args
        assert args[1] == "locals"
        assert "local_var" in args[0]
        assert args[0]["local_var"] == "hello"


def test_explorer_truediv_with_name() -> None:
    """The explorer should use __name__ if available."""

    class NamedObj:
        __name__ = "Named"

    explorer = InteractiveExplorer()
    obj = NamedObj()

    with patch.object(InteractiveExplorer, "_run") as mock_run:
        result = explorer / obj
        assert result is obj
        mock_run.assert_called_once_with(obj, "Named")


@patch("sus_inspector.tui.app.ObjectExplorerApp")
def test_explorer_run_starts_app(mock_app_class: MagicMock) -> None:
    """_run should initialize and run the Textual app."""
    mock_app_instance = mock_app_class.return_value
    explorer = InteractiveExplorer()
    obj = {"key": "value"}

    explorer._run(obj, "test")

    mock_app_class.assert_called_once_with(obj, obj_name="test")
    mock_app_instance.run.assert_called_once()
