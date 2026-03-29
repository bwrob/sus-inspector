"""Custom Textual widgets for sus-inspector."""

from __future__ import annotations

from typing import Any

from rich.panel import Panel
from rich.text import Text
from textual.containers import VerticalScroll
from textual.widgets import Static

from sus_inspector.hooks.registry import CLASS_HOOKS, get_renderer
from sus_inspector.metadata import ClassMetadata, get_class_metadata


class ClassInfoPane(VerticalScroll):
    """A pane to display class-level metadata."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the class info pane."""
        super().__init__(**kwargs)
        self.display = False

    def update_object(self, obj: Any) -> None:
        """Update the pane with a new object's class metadata.

        Args:
            obj: The object whose class metadata to display.

        """
        # Clear existing content
        self.query("*").remove()

        if obj is None:
            self.mount(Static("No class metadata for None."))
            return

        # Check for custom class renderer
        renderer = get_renderer(obj, CLASS_HOOKS)
        if renderer:
            self.mount(Static(renderer(obj)))
            return

        # Fallback to default class metadata extraction
        metadata = get_class_metadata(obj)
        self._mount_default(metadata)

    def _mount_default(self, metadata: ClassMetadata) -> None:
        """Mount default metadata sections.

        Args:
            metadata: The extracted class metadata.

        """
        # Docstring
        if metadata.doc:
            self.mount(
                Static(Panel(Text(metadata.doc, style="italic"), title="Docstring"))
            )

        # MRO and Inheritance Tree
        self.mount(
            Static(Panel(metadata.inheritance_tree, title="Inheritance Hierarchy"))
        )

        # Class Fields and Methods
        if metadata.class_fields:
            fields_text = Text(
                "\n".join(
                    f"{k}: {type(v).__name__}" for k, v in metadata.class_fields.items()
                )
            )
            self.mount(Static(Panel(fields_text, title="Class Fields")))

        if metadata.class_methods:
            methods_text = Text("\n".join(metadata.class_methods))
            self.mount(Static(Panel(methods_text, title="Class Methods")))
