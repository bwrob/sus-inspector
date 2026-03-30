"""Tests to verify the package distribution and entry points."""

from __future__ import annotations

import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest


@pytest.mark.skipif(sys.version_info < (3, 11), reason="tomllib requires Python 3.11+")
def test_entry_point_resolution() -> None:
    """The 'sus' entry point in pyproject.toml should point to a valid function.

    Raises:
        AssertionError: If the entry point is missing or invalid.

    """
    import tomllib  # noqa: PLC0415 # pyright: ignore[reportMissingTypeStubs] # ty: ignore[unresolved-import]

    root_dir = Path(__file__).parent.parent
    pyproject_path = root_dir / "pyproject.toml"

    assert pyproject_path.exists(), "pyproject.toml not found"

    with pyproject_path.open("rb") as f:
        pyproject: dict[str, Any] = tomllib.load(f)

    project: dict[str, Any] = pyproject.get("project", {})
    scripts: dict[str, Any] = project.get("scripts", {})
    sus_entry: str | None = scripts.get("sus")

    assert sus_entry is not None, "Entry point 'sus' not found in [project.scripts]"

    # Verify the module and function exist
    msg = f"Entry point '{sus_entry}' must be in 'module:func' format"
    assert ":" in sus_entry, msg

    module_name, func_name = sus_entry.split(":")

    # Check if the module exists
    spec = importlib.util.find_spec(module_name)
    msg = f"Module '{module_name}' referenced by entry point not found"
    assert spec is not None, msg

    # Load the module and check for the function
    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        pytest_fail_msg = f"Could not import module '{module_name}': {e}"
        raise AssertionError(pytest_fail_msg) from e

    assert hasattr(module, func_name), (
        f"Function '{func_name}' not found in module '{module_name}'"
    )
