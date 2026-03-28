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
    import sys

    # If run as a script, we can inspect locals or a simple object
    sus / sys.modules
