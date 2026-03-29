"""Tests for the CLI and global injection logic."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from sus_inspector.cli import (
    INJECTION_MARKER,
    _check_already_injected,  # pyright: ignore[reportPrivateUsage] # noqa: PLC2701
    _ensure_dir,  # pyright: ignore[reportPrivateUsage] # noqa: PLC2701
    _write_injection,  # pyright: ignore[reportPrivateUsage] # noqa: PLC2701
    get_injection_code,
    get_target_info,
    inject_permanently,
    remove_injection,
)


def test_get_injection_code() -> None:
    """Injection code should contain the marker and sus import."""
    code = get_injection_code()
    assert INJECTION_MARKER in code
    assert "from sus_inspector import sus" in code


def test_get_target_info() -> None:
    """get_target_info should return different paths for global/local."""
    with (
        patch("site.getusersitepackages", return_value="/user/site"),
        patch("site.getsitepackages", return_value=["/env/site"]),
    ):
        dir_global, file_global = get_target_info(is_global_user=True)
        assert dir_global == Path("/user/site")
        assert file_global == "usercustomize.py"

        dir_local, file_local = get_target_info(is_global_user=False)
        assert dir_local == Path("/env/site")
        assert file_local == "sitecustomize.py"

    # Test empty site_packages fallback
    with (
        patch("site.getusersitepackages", return_value="/user/site"),
        patch("site.getsitepackages", return_value=[]),
    ):
        dir_local, _ = get_target_info(is_global_user=False)
        assert dir_local == Path("/user/site")


def test_ensure_dir(tmp_path: Path) -> None:
    """_ensure_dir should create the directory if it doesn't exist."""
    target = tmp_path / "new_dir"
    assert _ensure_dir(target) is True
    assert target.exists()

    # Test failure (e.g., permission error)
    with patch.object(Path, "mkdir", side_effect=OSError("Perm error")):
        assert _ensure_dir(tmp_path / "fail_dir") is False


def test_check_already_injected(tmp_path: Path) -> None:
    """_check_already_injected should detect the marker."""
    f = tmp_path / "test.py"
    assert _check_already_injected(f, "test.py") is False

    _ = f.write_text(f"some code\n{INJECTION_MARKER}\nmore code")
    assert _check_already_injected(f, "test.py") is True


def test_write_injection(tmp_path: Path) -> None:
    """_write_injection should append the code."""
    f = tmp_path / "test.py"
    _ = f.write_text("existing content")

    _write_injection(f)
    content = f.read_text()
    assert "existing content" in content
    assert INJECTION_MARKER in content

    # Test failure
    with (
        patch.object(Path, "open", side_effect=OSError("Fail")),
        pytest.raises(SystemExit),
    ):
        _write_injection(f)


@patch("sus_inspector.cli.Confirm.ask", return_value=True)
@patch("sus_inspector.cli.get_target_info")
@patch("sus_inspector.cli._ensure_dir")
@patch("sus_inspector.cli._check_already_injected", return_value=False)
@patch("sus_inspector.cli._write_injection")
def test_inject_permanently(  # noqa: PLR0913, PLR0917
    mock_write: MagicMock,
    mock_check: MagicMock,
    mock_ensure: MagicMock,
    mock_info: MagicMock,
    mock_confirm: MagicMock,
    tmp_path: Path,
) -> None:
    """inject_permanently should follow the full flow."""
    target_dir = tmp_path / "site"
    mock_info.return_value = (target_dir, "test.py")
    mock_ensure.return_value = True

    inject_permanently(is_global_user=False)

    mock_write.assert_called_once_with(target_dir / "test.py")

    # Test ensure_dir failure
    mock_ensure.return_value = False
    with pytest.raises(SystemExit):
        inject_permanently()

    # Test already injected
    mock_ensure.return_value = True
    mock_check.return_value = True
    inject_permanently()
    assert mock_write.call_count == 1  # Still 1

    # Test abort
    mock_confirm.return_value = False
    inject_permanently()
    assert mock_write.call_count == 1


def test_remove_injection(tmp_path: Path) -> None:
    """remove_injection should remove the block."""
    f = tmp_path / "test.py"

    # Not existing
    with patch(
        "sus_inspector.cli.get_target_info", return_value=(tmp_path, "not_here.py")
    ):
        remove_injection(is_global_user=False)

    # No injection found
    _ = f.write_text("no injection here")
    with patch("sus_inspector.cli.get_target_info", return_value=(tmp_path, "test.py")):
        remove_injection()
        assert f.read_text() == "no injection here"

    # Injection found
    _ = f.write_text(f"start\n{get_injection_code()}\nend")
    with patch("sus_inspector.cli.get_target_info", return_value=(tmp_path, "test.py")):
        remove_injection()
        content = f.read_text()
        assert INJECTION_MARKER not in content
        assert "start" in content
        assert "end" in content

    # Test error on write
    _ = f.write_text(f"start\n{get_injection_code()}\nend")
    orig_open = Path.open

    def mocked_open(
        self: Path,
        *args: Any,  # noqa: ANN401
        **kwargs: Any,  # noqa: ANN401
    ) -> Any:  # noqa: ANN401
        if self == f and args and args[0] == "w":
            msg = "Write fail"
            raise OSError(msg)
        return orig_open(self, *args, **kwargs)  # pyright: ignore[reportUnknownVariableType]

    with (
        patch.object(Path, "open", side_effect=mocked_open, autospec=True),
        patch("sus_inspector.cli.get_target_info", return_value=(tmp_path, "test.py")),
        pytest.raises(SystemExit),
    ):
        remove_injection()
