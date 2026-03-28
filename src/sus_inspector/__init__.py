"""sus-inspector: The interactive, terminal-based object inspector.

Import `sus` to start exploring suspicious Python objects.
"""

from __future__ import annotations

from sus_inspector.hooks import register_hook
from sus_inspector.instances import sus

__all__ = ["register_hook", "sus"]
