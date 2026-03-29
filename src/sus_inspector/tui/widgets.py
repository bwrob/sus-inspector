"""Custom Textual widgets for sus-inspector."""

from __future__ import annotations

from typing import Any

from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.text import Text
from textual.widgets import Static

from sus_inspector.hooks.registry import CLASS_HOOKS, get_renderer
from sus_inspector.metadata import ClassMetadata, get_class_metadata


class ClassInfoPane(Static):
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
        if obj is None:
            self.update("No class metadata for None.")
            return

        # Check for custom class renderer
        renderer = get_renderer(obj, CLASS_HOOKS)
        if renderer:
            self.update(renderer(obj))
            return

        # Fallback to default class metadata extraction
        metadata = get_class_metadata(obj)
        self.update(self._render_default(metadata))

    def _render_default(self, metadata: ClassMetadata) -> RenderableType:
        """Default rendering for class metadata.

        Args:
            metadata: The extracted class metadata.

        Returns:
            RenderableType: Rich renderable for the metadata.

        """
        sections: list[RenderableType] = []

        # Docstring
        if metadata.doc:
            sections.append(
                Panel(Text(metadata.doc, style="italic"), title="Docstring")
            )

        # MRO and Inheritance Tree
        sections.append(Panel(metadata.inheritance_tree, title="Inheritance Hierarchy"))

        # Class Fields and Methods
        if metadata.class_fields:
            fields_text = Text(
                "\n".join(
                    f"{k}: {type(v).__name__}" for k, v in metadata.class_fields.items()
                )
            )
            sections.append(Panel(fields_text, title="Class Fields"))

        if metadata.class_methods:
            methods_text = Text("\n".join(metadata.class_methods))
            sections.append(Panel(methods_text, title="Class Methods"))

        return Group(*sections)
