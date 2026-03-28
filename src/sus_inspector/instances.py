"""Global instances for sus-inspector."""

from __future__ import annotations

from sus_inspector.core import InteractiveExplorer

# Create the global singleton.
# No hooks are registered here to keep it zero-cost.
sus = InteractiveExplorer()
