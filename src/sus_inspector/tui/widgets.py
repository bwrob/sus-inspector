"""Custom Textual widgets for sus-inspector."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast, final

from rich.panel import Panel
from rich.text import Text
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Input, OptionList, Static

if TYPE_CHECKING:
    from textual.app import ComposeResult
    from textual.widgets.tree import TreeNode

    from sus_inspector.hooks.registry import CLASS_HOOKS, get_renderer
from sus_inspector.hooks.registry import CLASS_HOOKS, get_renderer
from sus_inspector.metadata import ClassMetadata, get_class_metadata


@final
class NodeButton(Button):
    """A button that holds a reference to a tree node."""

    def __init__(
        self,
        label: str | None = None,
        *,
        node: TreeNode[object],
        variant: str = "default",
        name: str | None = None,
        widget_id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Initialize NodeButton."""
        super().__init__(
            label=label,
            variant=cast("Any", variant),
            name=name,
            id=widget_id,
            classes=classes,
            disabled=disabled,
        )
        self.node = node


@final
class Breadcrumbs(Horizontal):
    """A widget to display the current traversal path as clickable breadcrumbs."""

    def update_path(self, node: TreeNode[object]) -> None:
        """Update the breadcrumbs based on the selected node.

        Args:
            node: The currently selected tree node.

        """
        self.query("*").remove()

        path_nodes: list[TreeNode[object]] = []
        curr = node
        while curr:
            path_nodes.insert(0, curr)
            curr = curr.parent

        for i, p_node in enumerate(path_nodes):
            if i > 0:
                _ = self.mount(Static(" > ", classes="bc-separator"))

            label = str(p_node.label)
            # Remove Rich tags for button label for cleaner look in breadcrumbs
            import re  # noqa: PLC0415

            clean_label = re.sub(r"\[.*?\]", "", label)

            btn = NodeButton(
                clean_label, variant="default", classes="bc-button", node=p_node
            )
            _ = self.mount(btn)


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


@final
class HistoryModal(ModalScreen["TreeNode[object]"]):
    """A modal screen showing session history."""

    def __init__(self, history: list[TreeNode[object]]) -> None:
        """Initialize the history modal.

        Args:
            history: List of visited nodes.

        """
        super().__init__()
        self.history = history
        self.filtered_history: list[TreeNode[object]] = list(reversed(history))

    def compose(self) -> ComposeResult:
        """Compose the modal layout.

        Yields:
            Widgets for the history modal.

        """
        with Vertical(id="history-container"):
            yield Static("Session History", id="history-title")
            yield Input(placeholder="Search history...", id="history-search")
            # Use OptionList for efficient selection
            options = []
            for node in self.filtered_history:
                label = self._get_node_path(node)
                options.append(label)

            yield OptionList(*options, id="history-list")
            yield Static("Press Enter to select, Escape to cancel", id="history-footer")

    def on_mount(self) -> None:
        """Focus the search bar on mount."""
        _ = self.query_one("#history-search").focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Filter the history list as the user types.

        Args:
            event: Input change event.

        """
        query = event.value.lower()
        option_list = self.query_one(OptionList)
        _ = option_list.clear_options()

        self.filtered_history = []
        for node in reversed(self.history):
            path = self._get_node_path(node)
            if query in path.lower():
                _ = option_list.add_option(path)
                self.filtered_history.append(node)

    def _get_node_path(self, node: TreeNode[object]) -> str:
        """Get the full path string for a node.

        Args:
            node: The tree node.

        Returns:
            str: Path representation.

        """
        segments = []
        curr = node
        while curr and curr.parent:
            segments.insert(0, str(curr.label))
            curr = curr.parent

        path = "root"
        for s in segments:
            import re  # noqa: PLC0415

            clean_s = re.sub(r"\[.*?\]", "", s)
            if clean_s.startswith("["):
                path += clean_s
            else:
                path += f".{clean_s}"
        return path

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle option selection.

        Args:
            event: Selection event.

        """
        # We need to map back to the TreeNode via filtered_history
        self.dismiss(self.filtered_history[event.option_index])
