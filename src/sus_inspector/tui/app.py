"""The main Textual UI application for object exploration."""

from __future__ import annotations

import contextlib
import inspect
import logging
from typing import TYPE_CHECKING, Any, ClassVar, cast

from rich.panel import Panel
from rich.pretty import Pretty
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Footer, Header, Input, Static, Tree
from typing_extensions import override

from sus_inspector.hooks.handlers import HANDLER_REGISTRY, ensure_handlers
from sus_inspector.hooks.registry import VIEW_HOOKS, ensure_default_hooks
from sus_inspector.tui.widgets import (
    Breadcrumbs,
    ClassInfoPane,
    HistoryModal,
)

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
        Binding("d", "toggle_private", "Toggle Private Members"),
        Binding("c", "toggle_class_view", "Toggle Class Info"),
        Binding("e", "toggle_expansion", "Expand/Collapse Detail"),
        Binding("alt+left", "go_back", "Back", show=True),
        Binding("alt+right", "go_forward", "Forward", show=True),
        Binding("ctrl+h", "show_history", "History", show=True),
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
        self.show_private: bool = False
        self.grouping_threshold: int = 10
        self.history: list[TreeNode[object]] = []
        self.history_index: int = -1

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

        with Vertical():
            yield Breadcrumbs(id="breadcrumbs")

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

        msg = "Search keys (Press Enter to find next)..."
        yield Input(placeholder=msg, id="search-bar")
        yield Footer()

    async def on_mount(self) -> None:
        """Initialize the tree root."""
        tree = self.query_one(Tree[object])
        tree.root.data = self.root_obj
        self.add_children(tree.root, self.root_obj)
        _ = tree.root.expand()
        _ = tree.focus()

        # Ensure breadcrumbs are showing root on startup
        breadcrumbs = self.query_one(Breadcrumbs)
        _ = self.call_after_refresh(breadcrumbs.update_path, tree.root)

    def action_search(self) -> None:
        """Triggered by pressing '/' to show the search bar."""
        search_bar = self.query_one("#search-bar", Input)
        search_bar.display = True
        _ = search_bar.focus()

    async def action_toggle_class_view(self) -> None:
        """Toggle the class info pane."""
        pane = self.query_one(ClassInfoPane)
        pane.is_pane_visible = not pane.is_pane_visible
        if pane.is_pane_visible:
            tree = self.query_one(Tree[object])
            if tree.cursor_node:
                await pane.update_object(tree.cursor_node.data)

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

    def action_go_back(self) -> None:
        """Navigate back in history."""
        if self.history_index > 0:
            self.history_index -= 1
            tree = self.query_one(Tree[object])
            target_node = self.history[self.history_index]
            # Ensure path to node is expanded
            curr = target_node.parent
            while curr:
                _ = curr.expand()
                curr = curr.parent
            _ = tree.select_node(target_node)
            _ = tree.scroll_to_node(target_node)
            _ = tree.focus()

    def action_go_forward(self) -> None:
        """Navigate forward in history."""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            tree = self.query_one(Tree[object])
            target_node = self.history[self.history_index]
            # Ensure path to node is expanded
            curr = target_node.parent
            while curr:
                _ = curr.expand()
                curr = curr.parent
            _ = tree.select_node(target_node)
            _ = tree.scroll_to_node(target_node)
            _ = tree.focus()

    def action_show_history(self) -> None:
        """Show the session history modal."""

        def on_selected(node: TreeNode[object] | None) -> None:
            if node:
                tree = self.query_one(Tree[object])
                # Find the node in history and update index
                with contextlib.suppress(ValueError):
                    self.history_index = self.history.index(node)

                # Ensure path to node is expanded
                curr = node.parent
                while curr:
                    _ = curr.expand()
                    curr = curr.parent

                _ = tree.select_node(node)
                _ = tree.focus()

        _ = self.push_screen(HistoryModal(self.history, self.root_name), on_selected)

    def _push_history(self, node: TreeNode[object]) -> None:
        """Push a node to the navigation history.

        Args:
            node: The node to push.

        """
        if node.data is None:
            return

        # If we are already at this node in history, don't push.
        # This handles both history navigation and repeated clicks.
        if (
            0 <= self.history_index < len(self.history)
            and self.history[self.history_index] == node
        ):
            return

        # Truncate forward history if in middle
        # and navigating to a new place.
        self.history = self.history[: self.history_index + 1]
        self.history.append(node)
        self.history_index += 1

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

    def action_toggle_private(self) -> None:
        """Toggle the visibility of private members."""
        self.show_private = not self.show_private
        # Clear history as the tree is rebuilt and nodes are invalidated
        self.history = []
        self.history_index = -1
        tree = self.query_one(Tree[object])
        tree.root.remove_children()
        # Always re-populate from root object to reflect the toggle
        self.add_children(tree.root, self.root_obj)
        _ = tree.root.expand()
        _ = tree.refresh()

    def add_children(self, node: TreeNode[object], obj: object) -> None:
        """Recursively add children to a tree node.

        Args:
            node: The current tree node.
            obj: The object whose members to add.

        """
        handler = HANDLER_REGISTRY.get_handler(obj)
        if handler:
            self._add_handler_fields(node, obj, handler)
            return

        if isinstance(obj, dict):
            self._add_dict_children(node, cast("dict[object, object]", obj))
            return
        if isinstance(obj, (list, tuple, set)):
            self._add_collection_children(node, list(cast("list[object]", obj)))
            return

        self._add_smart_grouped_attributes(node, obj)

    def _add_smart_grouped_attributes(
        self, node: TreeNode[object], obj: object
    ) -> None:
        """Add object attributes using smart grouping and filtering."""
        fields, methods = self._partition_members(obj)
        total = len(fields) + len(methods)

        if total >= self.grouping_threshold:
            self._add_grouped_nodes(node, fields, methods)
        else:
            self._add_flat_nodes(node, fields, methods)

    def _partition_members(
        self, obj: object
    ) -> tuple[list[tuple[str, Any]], list[tuple[str, Any]]]:
        """Partition object members into fields and methods.

        Returns:
            tuple: Sorted lists of (name, value) for fields and methods.

        """
        all_names = dir(obj)
        if not self.show_private:
            boilerplate = {
                "__pydantic_initialised__",
                "__pydantic_fields_set__",
                "__pydantic_extra__",
                "__pydantic_private__",
            }
            all_names = [
                n for n in all_names if not n.startswith("_") and n not in boilerplate
            ]

        fields: list[tuple[str, Any]] = []
        methods: list[tuple[str, Any]] = []

        for name in all_names:
            try:
                val = getattr(obj, name)
                if inspect.isroutine(val):
                    methods.append((name, val))
                else:
                    fields.append((name, val))
            except Exception:  # noqa: BLE001, PERF203
                # Skip attributes that raise exceptions on access
                logger.debug("Failed to get attribute %s from %s", name, obj)
                continue

        return sorted(fields), sorted(methods)

    def _add_grouped_nodes(
        self,
        node: TreeNode[object],
        fields: list[tuple[str, Any]],
        methods: list[tuple[str, Any]],
    ) -> None:
        """Add virtual nodes for fields and methods."""
        if fields:
            f_node = node.add(
                f"📁 Fields ({len(fields)})",
                data=None,
                allow_expand=True,
            )
            for name, val in fields:
                _ = f_node.add(
                    f"• [cyan]{name}[/cyan]",
                    data=val,
                    allow_expand=self._is_expandable(val),
                )
            _ = f_node.expand()
        if methods:
            m_node = node.add(
                f"📁 Methods ({len(methods)})",
                data=None,
                allow_expand=True,
            )
            for name, val in methods:
                _ = m_node.add(
                    f"ƒ [magenta]{name}[/magenta]",
                    data=val,
                    allow_expand=self._is_expandable(val),
                )

    def _add_flat_nodes(
        self,
        node: TreeNode[object],
        fields: list[tuple[str, Any]],
        methods: list[tuple[str, Any]],
    ) -> None:
        """Add fields and methods directly to the node."""
        for name, val in fields:
            _ = node.add(
                f"• [cyan]{name}[/cyan]",
                data=val,
                allow_expand=self._is_expandable(val),
            )
        for name, val in methods:
            _ = node.add(
                f"ƒ [magenta]{name}[/magenta]",
                data=val,
                allow_expand=self._is_expandable(val),
            )

    def _add_handler_fields(
        self,
        node: TreeNode[object],
        obj: object,
        handler: Any,  # noqa: ANN401
    ) -> None:
        """Add fields from a specialized handler."""
        fields = list(handler.get_fields(obj).items())
        for k, v in fields[:MAX_TREE_CHILDREN]:
            _ = node.add(
                f"• [cyan]{k}[/cyan]", data=v, allow_expand=self._is_expandable(v)
            )
        if len(fields) > MAX_TREE_CHILDREN:
            _ = node.add(
                f"... and {len(fields) - MAX_TREE_CHILDREN} more fields",
                data=None,
                allow_expand=False,
            )

        # Add methods
        methods = handler.get_methods(obj)
        if methods:
            methods_node = node.add("📁 Methods", data=None, allow_expand=True)
            for name, func in sorted(methods.items()):
                _ = methods_node.add(
                    f"ƒ [magenta]{name}[/magenta]", data=func, allow_expand=False
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

    def on_button_pressed(self, _event: Button.Pressed) -> None:
        """Handle button press events."""
        # Generic button handler if needed

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
        _ = self.run_worker(
            self.on_tree_node_highlighted(Tree.NodeHighlighted(tree.cursor_node))
        )

    async def on_tree_node_highlighted(
        self, event: Tree.NodeHighlighted[object]
    ) -> None:
        """Update the detail view when a node is highlighted.

        Args:
            event: Highlight event.

        """
        # --- Update History & Breadcrumbs Immediately ---
        self._push_history(event.node)
        breadcrumbs = self.query_one(Breadcrumbs)
        await breadcrumbs.update_path(event.node)

        detail_view = self.query_one("#detail-view", Static)
        detail_pane = self.query_one("#detail-pane")
        class_pane = self.query_one(ClassInfoPane)
        obj = event.node.data

        # --- Update the Class Info Pane (if visible) ---
        if class_pane.is_pane_visible:
            await class_pane.update_object(obj)

        # --- Handle the Data View ---
        if obj is None:
            detail_pane.border_subtitle = "NoneType"
            detail_view.update("No data.")
            return

        detail_pane.border_subtitle = f"Type: {type(obj).__name__}"

        handler = HANDLER_REGISTRY.get_handler(obj)
        if handler:
            expanded = id(obj) in self.expanded_details
            detail_view.update(handler.render(obj, expanded=expanded))
            return

        if self._try_view_hooks(detail_view, obj):
            return

        # Fallback to rich pretty print
        detail_view.update(Panel(Pretty(obj), title="Object Preview"))

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
