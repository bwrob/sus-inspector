# Implementation Plan: Collapsible Class Information Pane with Double Registry

## Phase 1: Research & Double Registry Design
- [x] Task: Design the Double Registry system.
    - [x] Create a feature branch `feat/double-registry`.
    - [x] Define separate registry objects for instance and class-level inspectors.
    - [x] Implement a lookup mechanism that falls back to default inspectors if a specific one is not found.
    - [x] Write unit tests for the double registry (various combinations of custom and default).
- [x] Task: Conductor - User Manual Verification 'Research & Double Registry Design' (Protocol in workflow.md)

## Phase 2: Class Metadata Extraction & Rendering
- [x] Task: Implement a default class-level metadata extractor.
    - [x] Create a feature branch `feat/class-metadata-extractor`.
    - [x] Extract docstrings, class fields, class methods, MRO, and inheritance tree.
    - [x] Write tests to verify the extraction logic for complex class hierarchies.
- [x] Task: Implement the default class-level renderer (UI component).
    - [x] Design the layout (stacked) for displaying class metadata.
    - [x] Implement the `ClassInfoPane` Textual widget.
    - [x] Write TUI tests for rendering the class metadata correctly.
- [x] Task: Conductor - User Manual Verification 'Class Metadata Extraction & Rendering' (Protocol in workflow.md)

## Phase 3: TUI Integration & Key Bindings
- [x] Task: Integrate the `ClassInfoPane` into the main TUI.
    - [x] Create a feature branch `feat/tui-class-pane-integration`.
    - [x] Add the `ClassInfoPane` to the `Explorer` or `App` layout.
    - [x] Set its initial visibility to `False`.
    - [x] Map the 'c' key to toggle the `visible` property of the pane.
    - [x] Add a distinct colored border to the class pane.
    - [x] Write TUI tests for the 'c' key toggle behavior.
- [x] Task: Conductor - User Manual Verification 'TUI Integration & Key Bindings' (Protocol in workflow.md)

## Phase 4: Final Polish & Verification
- [x] Task: Refine the visual styling and interactions.
    - [x] Perform a full review for visual consistency and responsiveness.
    - [x] Ensure the pane behaves correctly with different terminal sizes and themes.
    - [x] Verify 95% test coverage (for new modules).
    - [x] Run full linting and type-checking suite.
- [x] Task: Conductor - User Manual Verification 'Final Polish & Verification' (Protocol in workflow.md)

## Phase: Review Fixes
- [x] Task: Apply review suggestions 6baf7dc
