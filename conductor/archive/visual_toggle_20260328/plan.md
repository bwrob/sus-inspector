# Implementation Plan: Visual Toggle ('d') and Smart Grouping

## Phase 1: Preparation & State Management
- [x] Task: Add state flags and threshold settings to `ObjectExplorerApp`.
    - [x] Add `show_private: bool = False`.
    - [x] Add `grouping_threshold: int = 10`.
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Tree Categorization & Grouping
- [x] Task: Implement smart categorization logic.
    - [x] Function to partition members into `fields` and `methods`.
    - [x] Implement logic to decide whether to group based on total count vs `grouping_threshold`.
- [x] Task: Update `ObjectExplorerApp.add_children` to support virtual nodes.
    - [x] Add "Fields (N)" and "Methods (M)" virtual nodes for large objects.
    - [x] Implement auto-expansion for the "Fields" node.
- [x] Task: Add visual styling to tree labels.
    - [x] Use `•` and `ƒ` prefixes and appropriate colors for fields vs methods.
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Bindings & UI Feedback
- [x] Task: Implement 'd' toggle and tree re-rendering.
    - [x] Refresh the tree when `show_private` changes.
    - [x] Update Footer/Status Bar with toggle state info.
- [x] Task: Write TUI tests for smart grouping.
    - [x] Verify that small objects stay flat.
    - [x] Verify that large objects (e.g., Pydantic models) get grouped.
    - [x] Verify 'd' toggle correctly hides/shows private members.
- [x] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Final Polish & Verification
- [x] Task: Refine Pydantic/Boilerplate noise filtering.
    - [x] Explicitly hide common internal dunders for cleaner view.
    - [x] Verify 95% test coverage.
    - [x] Final code quality check (`rtk poe code-quality`).
- [x] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)
