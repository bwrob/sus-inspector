"""Custom Textual widgets for sus-inspector."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, final

from rich.panel import Panel
from rich.text import Text
from textual.containers import VerticalScroll
from textual.widgets import Static

from sus_inspector.hooks.registry import CLASS_HOOKS, get_renderer
from sus_inspector.metadata import get_class_metadata

if TYPE_CHECKING:
    from sus_inspector.metadata import ClassMetadata


@final
class ClassInfoPane(VerticalScroll):
    """A pane to display class-level metadata."""

    _is_pane_visible: bool

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize the class info pane."""
        super().__init__(**kwargs)
        self._is_pane_visible = False
        self.display = False  # type: ignore[reportUnannotatedClassAttribute]

    @property
    def is_pane_visible(self) -> bool:
        """Check if the pane is currently visible."""
        return self._is_pane_visible

    @is_pane_visible.setter
    def is_pane_visible(self, value: bool) -> None:
        """Set the visibility of the pane."""
        self._is_pane_visible = value
        self.display = value

    def update_object(self, obj: object) -> None:
        """Update the pane with a new object's class metadata.

        Args:
            obj: The object whose class metadata to display.

        """
        # Clear existing content
        _ = self.query("*").remove()

        if obj is None:
            _ = self.mount(Static("No class metadata for None."))
            return

        # 1. Check for specialized handler class view
        from sus_inspector.hooks.handlers import HANDLER_REGISTRY  # noqa: PLC0415

        handler = HANDLER_REGISTRY.get_handler(obj)
        if handler:
            _ = self.mount(Static(handler.render_class_view(obj)))
            # We still want to show the base metadata (MRO, etc.)
            metadata = get_class_metadata(obj)
            self._mount_essential_metadata(metadata)
            return

        # 2. Check for custom class renderer (legacy hooks)
        renderer = get_renderer(obj, CLASS_HOOKS)
        if renderer:
            _ = self.mount(Static(renderer(obj)))
            return

        # 3. Fallback to default class metadata extraction
        metadata = get_class_metadata(obj)
        self._mount_default(metadata)

    def _mount_essential_metadata(self, metadata: ClassMetadata) -> None:
        """Mount essential metadata sections (MRO, docstring).

        Args:
            metadata: The extracted class metadata.

        """
        # Docstring
        if metadata.doc:
            _ = self.mount(
                Static(Panel(Text(metadata.doc, style="italic"), title="Docstring"))
            )

        # MRO and Inheritance Tree
        _ = self.mount(
            Static(Panel(metadata.inheritance_tree, title="Inheritance Hierarchy"))
        )

    def _mount_default(self, metadata: ClassMetadata) -> None:
        """Mount default metadata sections.

        Args:
            metadata: The extracted class metadata.

        """
        self._mount_essential_metadata(metadata)

        # Class Fields and Methods
        if metadata.class_fields:
            fields_text = Text(
                "\n".join(
                    f"{k}: {type(v).__name__}" for k, v in metadata.class_fields.items()
                )
            )
            _ = self.mount(Static(Panel(fields_text, title="Class Fields")))

        if metadata.class_methods:
            methods_text = Text("\n".join(metadata.class_methods))
            _ = self.mount(Static(Panel(methods_text, title="Class Methods")))
