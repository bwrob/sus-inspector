# Implementation Plan: Replace `rich.inspect` with Custom Inspector Registry

## Phase 1: Research & Core Registry Design
- [x] Task: Define the `InspectorRegistry` interface.
    - [x] Create a feature branch `feat/inspector-registry-core`.
    - [x] Design a simple registry mechanism (e.g., a dictionary mapping types to callables).
    - [x] Define the base `Inspector` protocol or abstract class.
    - [x] Write unit tests for the registry (adding/retrieving inspectors).
- [x] Task: Conductor - User Manual Verification 'Research & Core Registry Design' (Protocol in workflow.md)

## Phase 2: Built-in Type Inspectors
- [x] Task: Implement inspectors for basic Python types.
    - [x] Create a feature branch `feat/built-in-inspectors`.
    - [x] Implement `PrimitiveInspector` for `int`, `float`, `str`, `bool`, `None`.
    - [x] Implement `CollectionInspector` for `list`, `tuple`, `dict`, `set`.
    - [x] Write TDD tests to verify that these types render with the expected structure.
- [x] Task: Implement `ObjectInspector` for classes and instances.
    - [x] Research how `rich.inspect` extracts attributes and methods.
    - [x] Implement a custom inspector that extracts:
        - Docstrings.
        - Attributes (instance and class).
        - Methods (filtering private/dunder based on existing flags).
    - [x] Write tests to compare output with existing requirements.
- [x] Task: Conductor - User Manual Verification 'Built-in Type Inspectors' (Protocol in workflow.md)

## Phase 3: TUI Integration & Layout Refactor
- [x] Task: Update the TUI `Explorer` to use the new `InspectorRegistry`.
    - [x] Create a feature branch `feat/tui-layout-refactor`.
    - [x] Replace calls to `rich.inspect` with calls to the registry.
    - [x] Implement a custom TUI layout (e.g., side-by-side panels for attributes and methods).
    - [x] Verify the layout looks consistent and high-contrast.
- [x] Task: Implement specialized inspectors (e.g., Pydantic).
    - [x] Add a hook for Pydantic models (if installed).
    - [x] Write tests to verify correct rendering of Pydantic models.
- [x] Task: Conductor - User Manual Verification 'TUI Integration & Layout Refactor' (Protocol in workflow.md)

## Phase 4: Cleanup & Dependency Removal
- [x] Task: Systematically remove all `rich.inspect` imports.
    - [x] Create a feature branch `feat/cleanup-rich-inspect`.
    - [x] Search for and remove any remaining usages.
    - [x] Verify that the project still builds and runs without any errors.
- [x] Task: Final Polish & Verification.
    - [x] Perform a full site review for grammar, clarity, and consistency.
    - [x] Ensure all links and images are functioning correctly.
    - [x] Validate the site's responsiveness on different screen sizes.
- [x] Task: Conductor - User Manual Verification 'Final Polish & Verification' (Protocol in workflow.md)
