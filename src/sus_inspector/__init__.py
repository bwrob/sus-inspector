"""sus-inspector: The interactive, terminal-based object inspector.

Import `sus` to start exploring suspicious Python objects.
"""

from __future__ import annotations

from sus_inspector.core import InteractiveExplorer
from sus_inspector.hooks import register_hook
from sus_inspector.hooks.builtins import list_view

# Create the global singleton
sus = InteractiveExplorer()

# Register built-in hooks
register_hook(list, list_view)

# Optional Pydantic support
try:
    from pydantic import BaseModel

    from sus_inspector.hooks.pydantic import pydantic_view

    register_hook(BaseModel, pydantic_view)
except ImportError:
    pass

__all__ = ["register_hook", "sus"]


def main() -> None:
    """Entry point for the sus command line."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="sus",
        description="sus-inspector: The interactive terminal-based object inspector.",
        epilog="Use 'sus --inject' to make 'sus' available globally in your environment.",
    )
    parser.add_argument(
        "--inject",
        action="store_true",
        help="Inject 'sus' into builtins (targets venv by default).",
    )
    parser.add_argument(
        "--remove",
        action="store_true",
        help="Remove 'sus' global injection.",
    )
    parser.add_argument(
        "--global",
        dest="is_global",
        action="store_true",
        help="Target the global user-site instead of the virtual environment.",
    )

    args = parser.parse_args()

    if args.inject:
        from sus_inspector.cli import inject_permanently

        inject_permanently(is_global=args.is_global)
    elif args.remove:
        from sus_inspector.cli import remove_injection

        remove_injection(is_global=args.is_global)
    else:
        parser.print_help()
