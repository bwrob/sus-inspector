"""Tests for the main entry point."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

from sus_inspector.main import main


def test_main_inject() -> None:
    """Main should call inject_permanently if --inject is passed."""
    with (
        patch("argparse.ArgumentParser.parse_args") as mock_args,
        patch("sus_inspector.main.inject_permanently") as mock_inject,
    ):
        mock_args.return_value = MagicMock(
            inject=True, remove=False, is_global_user=True
        )
        main()
        mock_inject.assert_called_once_with(is_global_user=True)


def test_main_remove() -> None:
    """Main should call remove_injection if --remove is passed."""
    with (
        patch("argparse.ArgumentParser.parse_args") as mock_args,
        patch("sus_inspector.main.remove_injection") as mock_remove,
    ):
        mock_args.return_value = MagicMock(
            inject=False, remove=True, is_global_user=False
        )
        main()
        mock_remove.assert_called_once_with(is_global_user=False)


def test_main_default() -> None:
    """Main should call sus / sys.modules by default."""
    with (
        patch("argparse.ArgumentParser.parse_args") as mock_args,
        patch("sus_inspector.main.sus") as mock_sus,
    ):
        mock_args.return_value = MagicMock(
            inject=False, remove=False, is_global_user=False
        )
        main()
        # Verify operator overloading / call
        mock_sus.__truediv__.assert_called_once_with(sys.modules)
