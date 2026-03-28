"""sus-inspector CLI entry point."""

from __future__ import annotations

import argparse
import sys

from sus_inspector.cli import inject_permanently, remove_injection
from sus_inspector.instances import sus


def main() -> None:
    """Entry point for the sus command line."""
    desc = "sus-inspector: The interactive terminal-based object inspector."
    ep_msg = "Use 'sus --inject' to make 'sus' available globally in your environment."
    parser = argparse.ArgumentParser(
        prog="sus",
        description=desc,
        epilog=ep_msg,
    )
    _ = parser.add_argument(
        "--inject",
        action="store_true",
        help="Inject 'sus' into builtins (targets venv by default).",
    )
    _ = parser.add_argument(
        "--remove",
        action="store_true",
        help="Remove 'sus' global injection.",
    )
    _ = parser.add_argument(
        "--global",
        dest="is_global_user",
        action="store_true",
        help="Target the global user-site instead of the virtual environment.",
    )

    args = parser.parse_args()

    if getattr(args, "inject", False):
        inject_permanently(is_global_user=bool(getattr(args, "is_global_user", False)))
    elif getattr(args, "remove", False):
        remove_injection(is_global_user=bool(getattr(args, "is_global_user", False)))
    else:
        # Default behavior: Inspect current system modules
        _ = sus / sys.modules
