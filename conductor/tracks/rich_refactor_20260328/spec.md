# Specification: Replace `rich.inspect` with Custom Inspector Registry

## Overview
This track involves refactoring `sus-inspector` to remove all internal dependencies on `rich.inspect`. We will build a modular "Inspector Registry" that allows for object-specific rendering logic. This will provide better control over the visual style, enabling a custom TUI layout that better aligns with the project's goals.

## Functional Requirements
- **Registry System:** Implement a registry to map Python types (or categories of objects) to custom inspector functions/classes.
- **Visual Style:** Define a new, high-contrast visual layout for object inspection that is optimized for TUI display (e.g., using Textual widgets like `Static`, `Tree`, or side-by-side panels).
- **Core Inspectors:** Create initial inspectors for common Python types:
    - Built-in types (`list`, `dict`, `str`, `int`, etc.).
    - Classes and instances (methods, attributes, dunder methods).
    - Modules.
- **Registry Hooks:** Allow for easy extension to support third-party libraries (e.g., Pydantic).
- **Removal of `rich.inspect`:** Systematically replace all calls to `rich.inspect` with the new registry-based system.

## Non-Functional Requirements
- **Zero Friction:** The new system must be just as easy to use as the old one (ideally transparent to the user).
- **Performance:** Ensure that custom rendering logic is efficient and does not impact TUI responsiveness.
- **Maintainability:** The registry should be well-documented and easy for contributors to add new inspectors.

## Acceptance Criteria
- [ ] No calls to `rich.inspect` remain in the codebase.
- [ ] The `Inspector Registry` is implemented and functional.
- [ ] Core Python types render correctly using the new TUI-optimized layout.
- [ ] Regression tests pass, ensuring that critical information (attributes, methods) is still displayed.
- [ ] Dependency checks confirm that `rich.inspect` is not being imported or used in the core logic.
- [ ] Specialized rendering for at least one complex type (e.g., a Pydantic model) is verified.

## Out of Scope
- **Interactive Editing:** Modifying object attributes directly from the TUI is out of scope for this track.
- **Advanced Plotting:** Complex data visualization (e.g., charts) is not required.
