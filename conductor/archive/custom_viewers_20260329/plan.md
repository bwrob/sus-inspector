# Implementation Plan: Unified Custom Object Viewers (track/custom-viewers-20260329)

## Phase 1: Foundation & Generic Handler Interface
- [x] Task: Design the BaseObjectHandler interface and unified registry for specialized viewers.
    - [x] Define the base class for all library handlers.
    - [x] Implement a dynamic registry to detect and load handlers for available libraries.

- [x] Task: Implement the Complexity Heuristic.
    - [x] Create a utility to assess object complexity based on depth, field count, and size.
    - [x] Define a standard `is_complex()` check for all handlers.
- [x] Task: Implement the `dataclasses` Handler (Standard Library).
    - [x] Create a specialized handler for Python's `dataclasses.dataclass`.
    - [x] Ensure it correctly extracts fields and values.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Foundation & Generic Handler Interface' (Protocol in workflow.md)

## Phase 2: Library-Specific Specialized Handlers
- [x] Task: Implement the `Pydantic` Handler.
    - [x] Detect and handle `pydantic` (v1 and v2) `BaseModel` instances.
    - [x] Handle internal Pydantic metadata and configurations.
- [x] Task: Implement the `attrs` Handler.
    - [x] Add support for `attrs` (and its alias `attr`) classes.
    - [x] Correct extraction of fields and validation of attributes.
- [x] Task: Implement the `msgspec` Handler.
    - [x] Add support for `msgspec` structs.
    - [x] Ensure it handles highly optimized data structures without overhead.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Library-Specific Specialized Handlers' (Protocol in workflow.md)

## Phase 3: Interactive Tree Navigation & Dynamic Content
- [x] Task: Update the TUI for Nested Object Expansion.
    - [x] Refactor the Textual view to use a tree-like structure for nested objects.
    - [x] Implement keyboard/mouse triggers for expanding and collapsing nodes.
- [x] Task: Integrate Dynamic Content Logic.
    - [x] Use the complexity assessment to decide if an object should be initially collapsed.
    - [x] Ensure nested objects trigger their own library-specific handlers recursively.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Interactive Tree Navigation & Dynamic Content' (Protocol in workflow.md)

## Phase 4: Optimization & Verification
- [x] Task: Implement Lazy-Loading for Large Trees.
    - [x] Optimize the tree rendering to only process and render visible nodes.
    - [x] Ensure performance remains high for deeply nested or massive objects.
- [x] Task: Comprehensive Testing and Coverage.
    - [x] Write integration tests for all four libraries.
    - [x] Ensure at least 95% test coverage for the new logic.
- [x] Task: Final UI Polish & Styling.
    - [x] Apply consistent styling for library tags and headers across all viewers.
    - [x] Ensure cross-terminal compatibility for the expansion icons.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Optimization & Verification' (Protocol in workflow.md)
