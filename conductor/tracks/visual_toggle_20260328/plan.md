# Implementation Plan: Visual Toggle ('d') and Tree Grouping

## Phase 1: Preparation & State Management
- [ ] Task: Add state flags to the TUI `ObjectExplorerApp`.
    - [ ] Add `show_private: bool = False`.
    - [ ] Add `group_members: bool = True`.
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Tree Logic & Grouping
- [ ] Task: Implement method/field categorization.
    - [ ] Use `inspect.isroutine` to identify methods in `ObjectExplorerApp.add_children`.
- [ ] Task: Refactor `ObjectExplorerApp.add_children` to support grouping.
    - [ ] Create virtual "Fields" and "Methods" nodes for complex objects.
    - [ ] Ensure lazy loading still works correctly with grouping.
- [ ] Task: Implement private member filtering.
    - [ ] Filter out members starting with `_` unless `show_private` is `True`.
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: UI Integration & Bindings
- [ ] Task: Implement 'd' key binding logic.
    - [ ] Toggle `show_private` and trigger a tree refresh.
    - [ ] Update the `Footer` to show the current toggle status.
- [ ] Task: Write TUI tests for filtering and grouping.
    - [ ] Verify that fields and methods are correctly categorized.
    - [ ] Verify that toggling 'd' shows/hides the expected members.
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Final Polish & Verification
- [ ] Task: Refine visual feedback for toggle state.
    - [ ] Add indicators to the UI (e.g., status bar, footer).
    - [ ] Verify 95% test coverage.
    - [ ] Final code quality check (`rtk poe code-quality`).
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)
