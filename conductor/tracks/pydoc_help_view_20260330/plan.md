# Implementation Plan: Integrated PyDoc/Help View

## Phase 1: Help Extraction Logic
- [ ] Task: Implement `get_doc_info(obj: object)` using `pydoc.render_doc()`.
- [ ] Task: Write tests to verify documentation extraction for various object types (modules, classes, functions).
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: UI Integration (Help Pane)
- [ ] Task: Implement a new `HelpPane` Textual widget (inheriting from `VerticalScroll`).
- [ ] Task: Add 'h' key binding to toggle the help pane visibility.
- [ ] Task: Integrate with `ObjectExplorerApp.on_tree_node_highlighted` to update the help pane.
- [ ] Task: Write TUI tests for the help pane toggle and updates.
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Formatting & Syntax
- [ ] Task: Apply Rich formatting and syntax highlighting to the captured help text.
- [ ] Task: Ensure docstrings are visually consistent with the rest of the TUI.
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Final Polish
- [ ] Task: Final code quality check.
- [ ] Task: Verify 95% coverage for the doc extractor.
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)
