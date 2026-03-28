"""Global instances and default registrations for sus-inspector."""

from __future__ import annotations

from sus_inspector.core import InteractiveExplorer
from sus_inspector.hooks.builtins import list_view
from sus_inspector.hooks.registry import register_hook

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
