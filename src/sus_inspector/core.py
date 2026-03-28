"""Core logic for the sus-inspector explorer."""

from __future__ import annotations

import inspect

from sus_inspector.tui.app import ObjectExplorerApp


class InteractiveExplorer:
    """The main 'sus' interface supporting both calls and operator overloading."""

    def __call__(self, obj: object, name: str = "root") -> object:
        """Inspect the object via standard call: sus(obj, name='my_obj').

        Args:
            obj: Object to inspect.
            name: Label for the object.

        Returns:
            object: The object untouched.

        """
        self._run(obj, name)
        return obj

    def __truediv__(self, obj: object) -> object | None:
        """Operator overloading: sus / obj.

        Args:
            obj: Object to inspect or Ellipsis for locals.

        Returns:
            object | None: The object untouched, or None if Ellipsis was used.

        """
        if obj is Ellipsis:
            # Capture local variables from the caller's frame
            current_frame = inspect.currentframe()
            if current_frame and current_frame.f_back:
                frame = current_frame.f_back
                local_items = frame.f_locals.items()
                local_vars = {
                    str(k): v for k, v in local_items if not str(k).startswith("__")
                }
                self._run(local_vars, "locals")
            return None

        # Determine a reasonable default name
        name: str = "root"
        name = str(obj.__name__) if hasattr(obj, "__name__") else type(obj).__name__

        self._run(obj, name)
        return obj

    @staticmethod
    def _run(obj: object, name: str) -> None:
        """Start the Textual App.

        Args:
            obj: Object to explore.
            name: Root name for tree.

        """
        app = ObjectExplorerApp(obj, obj_name=name)
        app.run()
