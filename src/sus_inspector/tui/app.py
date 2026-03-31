"""The main Textual UI application for object exploration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, ClassVar, cast

from rich.panel import Panel
from rich.pretty import Pretty
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Footer, Header, Input, Static, Tree
from typing_extensions import override

from sus_inspector.hooks.registry import VIEW_HOOKS, ensure_default_hooks
from sus_inspector.tui.widgets import ClassInfoPane

if TYPE_CHECKING:
    from textual._path import CSSPathType
    from textual.widgets.tree import TreeNode

logger = logging.getLogger(__name__)

MAX_TREE_CHILDREN = 100


class ObjectExplorerApp(App[None]):
    """Textual TUI for exploring Python objects."""

    CSS_PATH: ClassVar[CSSPathType | None] = "styles.tcss"

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("q", "quit", "Quit"),
        Binding("escape", "quit", "Quit"),
        Binding("/", "search", "Search Tree"),
        Binding("c", "toggle_class_view", "Toggle Class Info"),
        Binding("e", "toggle_expansion", "Expand/Collapse Detail"),
        Binding("left", "tree_collapse", "Collapse Node", show=False, priority=True),
        Binding("right", "tree_expand", "Expand Node", show=False, priority=True),
    ]

    def __init__(
        self,
        obj: object,
        obj_name: str = "root",
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """Initialize the object explorer app.

        Args:
            obj: The object to explore.
            obj_name: Label for the root node.
            **kwargs: Additional args for Textual App.

        """
        super().__init__(**kwargs)
        self.root_obj: object = obj
        self.root_name: str = obj_name
        self.expanded_details: set[int] = set()
        # Ensure handlers are loaded when the app starts
        from sus_inspector.hooks.handlers import ensure_handlers  # noqa: PLC0415

        ensure_default_hooks()
        ensure_handlers()

    @override
    def compose(self) -> ComposeResult:
        """Compose the UI layout.

        Yields:
            Header: UI header.
            Horizontal: Main exploration panes.
            Static: Path bar.
            Input: Search bar.
            Footer: UI footer.

        """
        yield Header(show_clock=True, icon="🔍")

        with Horizontal():
            tree: Tree[object] = Tree(self.root_name, id="tree-pane")
            tree.border_title = "Object Tree"
            yield tree

            with Vertical(id="detail-container"):
                with VerticalScroll(id="detail-pane") as vs:
                    vs.border_title = "Inspection View"
                    vs.border_subtitle = "Select an item..."
                    yield Static("Select a node to inspect...", id="detail-view")

                class_pane = ClassInfoPane(id="class-pane")
                class_pane.border_title = "Class Information"
                yield class_pane

        yield Static(f"Path: {self.root_name}", id="path-bar")
        msg = "Search keys (Press Enter to find next)..."
        yield Input(placeholder=msg, id="search-bar")
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the tree root."""
        tree = self.query_one(Tree[object])
        tree.root.data = self.root_obj
        self.add_children(tree.root, self.root_obj)
        _ = tree.root.expand()
        _ = tree.focus()

    def action_search(self) -> None:
        """Triggered by pressing '/' to show the search bar."""
        search_bar = self.query_one("#search-bar", Input)
        search_bar.display = True
        _ = search_bar.focus()

    def action_toggle_class_view(self) -> None:
        """Toggle the class info pane."""
        pane = self.query_one(ClassInfoPane)
        pane.is_pane_visible = not pane.is_pane_visible
        if pane.is_pane_visible:
            tree = self.query_one(Tree[object])
            if tree.cursor_node:
                pane.update_object(tree.cursor_node.data)

    def action_tree_collapse(self) -> None:
        """Collapse the currently selected tree node."""
        tree = self.query_one(Tree[object])
        if tree.cursor_node:
            _ = tree.cursor_node.collapse()

    def action_tree_expand(self) -> None:
        """Expand the currently selected tree node."""
        tree = self.query_one(Tree[object])
        if tree.cursor_node:
            _ = tree.cursor_node.expand()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle search queries.

        Args:
            event: Input submission event.

        """
        query = event.value.lower()
        tree = self.query_one(Tree[object])
        search_bar = self.query_one("#search-bar", Input)

        def find_node(
            node: TreeNode[object],
            search_term: str,
        ) -> TreeNode[object] | None:
            if search_term in str(node.label).lower() and node != tree.root:
                return node
            for child in node.children:
                found = find_node(child, search_term)
                if found:
                    return found
            return None

        found_node = find_node(tree.root, query)

        if found_node:
            self._select_search_result(tree, found_node)

        search_bar.display = False
        search_bar.value = ""
        _ = tree.focus()

    @staticmethod
    def _select_search_result(
        tree: Tree[object],
        found_node: TreeNode[object],
    ) -> None:
        """Expand and scroll to search results.

        Args:
            tree: The tree widget.
            found_node: The node that matched.

        """
        curr = found_node.parent
        while curr:
            _ = curr.expand()
            curr = curr.parent
        _ = tree.select_node(found_node)
        _ = tree.scroll_to_node(found_node)

    def add_children(self, node: TreeNode[object], obj: object) -> None:
        """Recursively add children to a tree node.

        Args:
            node: The current tree node.
            obj: The object whose members to add.

        """
        from sus_inspector.hooks.handlers import HANDLER_REGISTRY  # noqa: PLC0415

        handler = HANDLER_REGISTRY.get_handler(obj)
        if handler:
            self._add_handler_fields(node, obj, handler)
            return

        if isinstance(obj, dict):
            self._add_dict_children(node, cast("dict[object, object]", obj))
        elif isinstance(obj, (list, tuple, set)):
            self._add_collection_children(node, list(cast("list[object]", obj)))
        else:
            self._add_object_attributes(node, obj)

    def _add_handler_fields(
        self,
        node: TreeNode[object],
        obj: object,
        handler: Any,  # noqa: ANN401
    ) -> None:
        """Add fields from a specialized handler."""
        fields = list(handler.get_fields(obj).items())
        for k, v in fields[:MAX_TREE_CHILDREN]:
            _ = node.add(str(k), data=v, allow_expand=self._is_expandable(v))
        if len(fields) > MAX_TREE_CHILDREN:
            _ = node.add(
                f"... and {len(fields) - MAX_TREE_CHILDREN} more fields",
                data=None,
                allow_expand=False,
            )

        # Add methods
        methods = handler.get_methods(obj)
        if methods:
            methods_node = node.add("Methods", data=None, allow_expand=False)
            for name, func in sorted(methods.items()):
                _ = methods_node.add(
                    f"{name}()",
                    data=func,
                    allow_expand=self._is_expandable(func),
                )

    def _add_dict_children(
        self, node: TreeNode[object], obj_dict: dict[object, object]
    ) -> None:
        """Add children from a dictionary."""
        items = list(obj_dict.items())
        for k, v in items[:MAX_TREE_CHILDREN]:
            _ = node.add(str(k), data=v, allow_expand=self._is_expandable(v))
        if len(items) > MAX_TREE_CHILDREN:
            _ = node.add(
                f"... and {len(items) - MAX_TREE_CHILDREN} more",
                data=None,
                allow_expand=False,
            )

    def _add_collection_children(
        self, node: TreeNode[object], obj_list: list[object]
    ) -> None:
        """Add children from a list/tuple/set."""
        for i, v in enumerate(obj_list[:MAX_TREE_CHILDREN]):
            _ = node.add(f"[{i}]", data=v, allow_expand=self._is_expandable(v))
        if len(obj_list) > MAX_TREE_CHILDREN:
            _ = node.add(
                f"... and {len(obj_list) - MAX_TREE_CHILDREN} more",
                data=None,
                allow_expand=False,
            )

    def _add_object_attributes(self, node: TreeNode[object], obj: object) -> None:
        """Add attributes of an object to the tree node.

        Args:
            node: The current tree node.
            obj: The object.

        """
        all_attrs = [a for p in [dir(obj)] for a in p if not a.startswith("_")]
        for attr_name in all_attrs[:MAX_TREE_CHILDREN]:
            try:
                attr_value = getattr(obj, attr_name)
                _ = node.add(
                    attr_name,
                    data=attr_value,
                    allow_expand=self._is_expandable(attr_value),
                )
            except AttributeError:  # noqa: PERF203 # pragma: no cover
                continue
            except Exception:  # pragma: no cover
                logger.exception(
                    "Failed to get attribute %s from %s", attr_name, obj
                )  # pragma: no cover
                continue  # pragma: no cover

        if len(all_attrs) > MAX_TREE_CHILDREN:
            _ = node.add(
                f"... and {len(all_attrs) - MAX_TREE_CHILDREN} more attributes",
                data=None,
                allow_expand=False,
            )

    @staticmethod
    def _is_expandable(obj: object) -> bool:
        """Check if an object can have children in the tree.

        Args:
            obj: Object to check.

        Returns:
            bool: True if expandable.

        """
        from sus_inspector.hooks.handlers import HANDLER_REGISTRY  # noqa: PLC0415

        if HANDLER_REGISTRY.get_handler(obj):
            return True

        if isinstance(obj, (dict, list, tuple, set)):
            obj_coll = cast("dict[object, object] | list[object]", obj)
            return len(obj_coll) > 0
        return bool(hasattr(obj, "__dict__")) or bool(hasattr(obj, "__slots__"))

    def on_tree_node_expanded(self, event: Tree.NodeExpanded[object]) -> None:
        """Lazy-load children when a node is expanded.

        Args:
            event: Expansion event.

        """
        if event.node.data is not None and not event.node.children:
            self.add_children(event.node, event.node.data)

    def action_toggle_expansion(self) -> None:
        """Toggle the expansion state of the current object in the detail view."""
        tree = self.query_one(Tree[object])
        if not tree.cursor_node:
            return

        obj_id = id(tree.cursor_node.data)
        if obj_id in self.expanded_details:
            self.expanded_details.remove(obj_id)
        else:
            self.expanded_details.add(obj_id)

        # Re-trigger highlight update to re-render the detail view
        self.on_tree_node_highlighted(Tree.NodeHighlighted(tree.cursor_node))

    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted[object]) -> None:
        """Update the detail view when a node is selected.

        Args:
            event: Highlight event.

        """
        detail_view = self.query_one("#detail-view", Static)
        detail_pane = self.query_one("#detail-pane")
        path_bar = self.query_one("#path-bar", Static)
        class_pane = self.query_one(ClassInfoPane)
        obj = event.node.data

        # --- Update the Tree Path Bar ---
        self._update_path_bar(path_bar, event.node)

        # --- Update the Class Info Pane (if visible) ---
        if class_pane.is_pane_visible:
            class_pane.update_object(obj)

        # --- Handle the Data View ---
        if obj is None:
            detail_pane.border_subtitle = "NoneType"
            detail_view.update("No data.")
            return

        detail_pane.border_subtitle = f"Type: {type(obj).__name__}"

        from sus_inspector.hooks.handlers import HANDLER_REGISTRY  # noqa: PLC0415

        handler = HANDLER_REGISTRY.get_handler(obj)
        if handler:
            expanded = id(obj) in self.expanded_details
            detail_view.update(handler.render(obj, expanded=expanded))
            return

        if self._try_view_hooks(detail_view, obj):
            return

        # Fallback to rich pretty print
        detail_view.update(Panel(Pretty(obj), title="Object Preview"))

    def _update_path_bar(self, path_bar: Static, node: TreeNode[object]) -> None:
        """Update the path bar with the current traversal path.

        Args:
            path_bar: Static widget for path.
            node: The currently selected node.

        """
        path_segments: list[str] = []
        curr = node
        while curr and curr.parent:
            path_segments.insert(0, str(curr.label))
            curr = curr.parent

        full_path: str = self.root_name
        for p in path_segments:
            if p.startswith("["):
                full_path += p
            else:
                full_path += f".{p}"
        path_bar.update(f"Path: {full_path}")

    @staticmethod
    def _try_view_hooks(detail_view: Static, obj: object) -> bool:
        """Try applying registered view hooks.

        Args:
            detail_view: Static widget for detail.
            obj: Object to render.

        Returns:
            bool: True if a hook was applied.

        """
        for type_checker, render_func in VIEW_HOOKS:
            matches = (
                isinstance(obj, type_checker)
                if isinstance(type_checker, type)
                else type_checker(obj)
            )
            if matches:
                try:
                    detail_view.update(render_func(obj))
                except Exception:
                    logger.exception("View hook %s failed for %s", render_func, obj)
                    continue
                else:
                    return True
        return False
