# Implementation Plan: Unified Custom Object Viewers (track/custom-viewers-20260329)

## Phase 1: Foundation & Generic Handler Interface
- [ ] Task: Design the `BaseObjectHandler` interface and unified registry for specialized viewers.
    - [ ] Define the base class for all library handlers.
    - [ ] Implement a dynamic registry to detect and load handlers for available libraries.
- [ ] Task: Implement the Complexity Heuristic.
    - [ ] Create a utility to assess object complexity based on depth, field count, and size.
    - [ ] Define a standard `is_complex()` check for all handlers.
- [ ] Task: Implement the `dataclasses` Handler (Standard Library).
    - [ ] Create a specialized handler for Python's `dataclasses.dataclass`.
    - [ ] Ensure it correctly extracts fields and values.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Foundation & Generic Handler Interface' (Protocol in workflow.md)

## Phase 2: Library-Specific Specialized Handlers
- [ ] Task: Implement the `Pydantic` Handler.
    - [ ] Detect and handle `pydantic` (v1 and v2) `BaseModel` instances.
    - [ ] Handle internal Pydantic metadata and configurations.
- [ ] Task: Implement the `attrs` Handler.
    - [ ] Add support for `attrs` (and its alias `attr`) classes.
    - [ ] Correct extraction of fields and validation of attributes.
- [ ] Task: Implement the `msgspec` Handler.
    - [ ] Add support for `msgspec` structs.
    - [ ] Ensure it handles highly optimized data structures without overhead.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Library-Specific Specialized Handlers' (Protocol in workflow.md)

## Phase 3: Interactive Tree Navigation & Dynamic Content
- [ ] Task: Update the TUI for Nested Object Expansion.
    - [ ] Refactor the Textual view to use a tree-like structure for nested objects.
    - [ ] Implement keyboard/mouse triggers for expanding and collapsing nodes.
- [ ] Task: Integrate Dynamic Content Logic.
    - [ ] Use the complexity assessment to decide if an object should be initially collapsed.
    - [ ] Ensure nested objects trigger their own library-specific handlers recursively.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Interactive Tree Navigation & Dynamic Content' (Protocol in workflow.md)

## Phase 4: Optimization & Verification
- [ ] Task: Implement Lazy-Loading for Large Trees.
    - [ ] Optimize the tree rendering to only process and render visible nodes.
    - [ ] Ensure performance remains high for deeply nested or massive objects.
- [ ] Task: Comprehensive Testing and Coverage.
    - [ ] Write integration tests for all four libraries.
    - [ ] Ensure at least 95% test coverage for the new logic.
- [ ] Task: Final UI Polish & Styling.
    - [ ] Apply consistent styling for library tags and headers across all viewers.
    - [ ] Ensure cross-terminal compatibility for the expansion icons.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Optimization & Verification' (Protocol in workflow.md)
