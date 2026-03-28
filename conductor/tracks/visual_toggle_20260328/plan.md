# Implementation Plan: Visual Toggle ('d')

## Phase 1: Preparation & Design
- [ ] Task: Define state management for private method visibility.
    - [ ] Add `show_private` boolean flag to the TUI `App` or `Explorer` class.
    - [ ] Set default state to `False`.
- [ ] Task: Conductor - User Manual Verification 'Preparation & Design' (Protocol in workflow.md)

## Phase 2: Core Logic & Key Bindings
- [ ] Task: Implement 'd' key binding in the TUI.
    - [ ] Create a feature branch `feat/visual-toggle-logic`.
    - [ ] Write tests for the toggle logic (independent of the UI if possible).
    - [ ] Map the 'd' key to a method that toggles the `show_private` flag.
    - [ ] Verify the flag toggles correctly.
- [ ] Task: Conductor - User Manual Verification 'Core Logic & Key Bindings' (Protocol in workflow.md)

## Phase 3: UI Integration
- [ ] Task: Update the object tree to respect the `show_private` flag.
    - [ ] Create a feature branch `feat/visual-toggle-ui`.
    - [ ] Modify the tree population logic to filter out items starting with `_` when `show_private` is `False`.
    - [ ] Trigger a refresh/re-population of the tree when the flag changes.
    - [ ] Write TUI tests (using Textual's testing utilities) to verify the filtering works.
- [ ] Task: Conductor - User Manual Verification 'UI Integration' (Protocol in workflow.md)

## Phase 4: Final Polish & Verification
- [ ] Task: Add visual feedback for the toggle state.
    - [ ] Add a status bar indicator or a subtle notification when the toggle is flipped.
    - [ ] Verify 95% test coverage.
    - [ ] Run full linting and type-checking suite.
- [ ] Task: Conductor - User Manual Verification 'Final Polish & Verification' (Protocol in workflow.md)
