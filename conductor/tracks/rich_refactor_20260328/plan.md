# Implementation Plan: Replace `rich.inspect` with Custom Inspector Registry

## Phase 1: Research & Core Registry Design
- [ ] Task: Define the `InspectorRegistry` interface.
    - [ ] Create a feature branch `feat/inspector-registry-core`.
    - [ ] Design a simple registry mechanism (e.g., a dictionary mapping types to callables).
    - [ ] Define the base `Inspector` protocol or abstract class.
    - [ ] Write unit tests for the registry (adding/retrieving inspectors).
- [ ] Task: Conductor - User Manual Verification 'Research & Core Registry Design' (Protocol in workflow.md)

## Phase 2: Built-in Type Inspectors
- [ ] Task: Implement inspectors for basic Python types.
    - [ ] Create a feature branch `feat/built-in-inspectors`.
    - [ ] Implement `PrimitiveInspector` for `int`, `float`, `str`, `bool`, `None`.
    - [ ] Implement `CollectionInspector` for `list`, `tuple`, `dict`, `set`.
    - [ ] Write TDD tests to verify that these types render with the expected structure.
- [ ] Task: Implement `ObjectInspector` for classes and instances.
    - [ ] Research how `rich.inspect` extracts attributes and methods.
    - [ ] Implement a custom inspector that extracts:
        - Docstrings.
        - Attributes (instance and class).
        - Methods (filtering private/dunder based on existing flags).
    - [ ] Write tests to compare output with existing requirements.
- [ ] Task: Conductor - User Manual Verification 'Built-in Type Inspectors' (Protocol in workflow.md)

## Phase 3: TUI Integration & Layout Refactor
- [ ] Task: Update the TUI `Explorer` to use the new `InspectorRegistry`.
    - [ ] Create a feature branch `feat/tui-layout-refactor`.
    - [ ] Replace calls to `rich.inspect` with calls to the registry.
    - [ ] Implement a custom TUI layout (e.g., side-by-side panels for attributes and methods).
    - [ ] Verify the layout looks consistent and high-contrast.
- [ ] Task: Implement specialized inspectors (e.g., Pydantic).
    - [ ] Add a hook for Pydantic models (if installed).
    - [ ] Write tests to verify correct rendering of Pydantic models.
- [ ] Task: Conductor - User Manual Verification 'TUI Integration & Layout Refactor' (Protocol in workflow.md)

## Phase 4: Cleanup & Dependency Removal
- [ ] Task: Systematically remove all `rich.inspect` imports.
    - [ ] Create a feature branch `feat/cleanup-rich-inspect`.
    - [ ] Search for and remove any remaining usages.
    - [ ] Verify that the project still builds and runs without any errors.
- [ ] Task: Final Polish & Verification.
    - [ ] Perform a full site review for grammar, clarity, and consistency.
    - [ ] Ensure all links and images are functioning correctly.
    - [ ] Validate the site's responsiveness on different screen sizes.
- [ ] Task: Conductor - User Manual Verification 'Final Polish & Verification' (Protocol in workflow.md)
