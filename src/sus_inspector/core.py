"""Core logic for the sus-inspector explorer."""

from __future__ import annotations

import inspect
from typing import Any

from sus_inspector.tui.app import ObjectExplorerApp


class InteractiveExplorer:
    """The main 'sus' interface supporting both calls and operator overloading."""

    def __call__(self, obj: Any, name: str = "root") -> Any:
        """Standard call: sus(obj, name='my_obj')."""
        self._run(obj, name)
        return obj

    def __truediv__(self, obj: Any) -> Any:
        """Operator overloading: sus / obj."""
        if obj is Ellipsis:
            # Capture local variables from the caller's frame
            frame = inspect.currentframe().f_back
            if frame:
                local_vars = {
                    k: v for k, v in frame.f_locals.items() if not k.startswith("__")
                }
                self._run(local_vars, "locals")
            return None

        # Determine a reasonable default name
        if hasattr(obj, "__name__"):
            name = str(obj.__name__)
        else:
            name = str(type(obj).__name__)

        self._run(obj, name)
        return obj

    def _run(self, obj: Any, name: str) -> None:
        """Start the Textual App."""
        app = ObjectExplorerApp(obj, obj_name=name)
        app.run()
