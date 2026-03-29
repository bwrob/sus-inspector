# Implementation Plan: Collapsible Class Information Pane with Double Registry

## Phase 1: Research & Double Registry Design
- [x] Task: Design the Double Registry system.
    - [x] Create a feature branch `feat/double-registry`.
    - [x] Define separate registry objects for instance and class-level inspectors.
    - [x] Implement a lookup mechanism that falls back to default inspectors if a specific one is not found.
    - [x] Write unit tests for the double registry (various combinations of custom and default).
- [x] Task: Conductor - User Manual Verification 'Research & Double Registry Design' (Protocol in workflow.md)

## Phase 2: Class Metadata Extraction & Rendering
- [ ] Task: Implement a default class-level metadata extractor.
    - [ ] Create a feature branch `feat/class-metadata-extractor`.
    - [ ] Extract docstrings, class fields, class methods, MRO, and inheritance tree.
    - [ ] Write tests to verify the extraction logic for complex class hierarchies.
- [ ] Task: Implement the default class-level renderer (UI component).
    - [ ] Design the layout (stacked) for displaying class metadata.
    - [ ] Implement the `ClassInfoPane` Textual widget.
    - [ ] Write TUI tests for rendering the class metadata correctly.
- [ ] Task: Conductor - User Manual Verification 'Class Metadata Extraction & Rendering' (Protocol in workflow.md)

## Phase 3: TUI Integration & Key Bindings
- [ ] Task: Integrate the `ClassInfoPane` into the main TUI.
    - [ ] Create a feature branch `feat/tui-class-pane-integration`.
    - [ ] Add the `ClassInfoPane` to the `Explorer` or `App` layout.
    - [ ] Set its initial visibility to `False`.
    - [ ] Map the 'c' key to toggle the `visible` property of the pane.
    - [ ] Add a distinct colored border to the class pane.
    - [ ] Write TUI tests for the 'c' key toggle behavior.
- [ ] Task: Conductor - User Manual Verification 'TUI Integration & Key Bindings' (Protocol in workflow.md)

## Phase 4: Final Polish & Verification
- [ ] Task: Refine the visual styling and interactions.
    - [ ] Perform a full review for visual consistency and responsiveness.
    - [ ] Ensure the pane behaves correctly with different terminal sizes and themes.
    - [ ] Verify 95% test coverage.
    - [ ] Run full linting and type-checking suite.
- [ ] Task: Conductor - User Manual Verification 'Final Polish & Verification' (Protocol in workflow.md)
