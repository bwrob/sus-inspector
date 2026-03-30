# Implementation Plan: Visual Toggle ('d') and Smart Grouping

## Phase 1: Preparation & State Management
- [ ] Task: Add state flags and threshold settings to `ObjectExplorerApp`.
    - [ ] Add `show_private: bool = False`.
    - [ ] Add `grouping_threshold: int = 10`.
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Tree Categorization & Grouping
- [ ] Task: Implement smart categorization logic.
    - [ ] Function to partition members into `fields` and `methods`.
    - [ ] Implement logic to decide whether to group based on total count vs `grouping_threshold`.
- [ ] Task: Update `ObjectExplorerApp.add_children` to support virtual nodes.
    - [ ] Add "Fields (N)" and "Methods (M)" virtual nodes for large objects.
    - [ ] Implement auto-expansion for the "Fields" node.
- [ ] Task: Add visual styling to tree labels.
    - [ ] Use `•` and `ƒ` prefixes and appropriate colors for fields vs methods.
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Bindings & UI Feedback
- [ ] Task: Implement 'd' toggle and tree re-rendering.
    - [ ] Refresh the tree when `show_private` changes.
    - [ ] Update Footer/Status Bar with toggle state info.
- [ ] Task: Write TUI tests for smart grouping.
    - [ ] Verify that small objects stay flat.
    - [ ] Verify that large objects (e.g., Pydantic models) get grouped.
    - [ ] Verify 'd' toggle correctly hides/shows private members.
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Final Polish & Verification
- [ ] Task: Refine Pydantic/Boilerplate noise filtering.
    - [ ] Explicitly hide common internal dunders for cleaner view.
    - [ ] Verify 95% test coverage.
    - [ ] Final code quality check (`rtk poe code-quality`).
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)
