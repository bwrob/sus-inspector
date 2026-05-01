# Specification: Architectural Review and Decoupling

## Overview
Refactor the `sus-inspector` codebase to improve architectural separation, reduce coupling, and enforce boundaries. The primary focus is to decouple the TUI from the core inspection logic and ensure that specific object handlers (e.g., Pydantic) are not directly referenced within the main TUI application.

## Functional Requirements
- **Decouple TUI and Core:** Ensure that `src/sus_inspector/tui/` does not have direct dependencies on the implementation details of core inspection or specific library hooks.
- **Specific Case Isolation:** Remove any explicit mentions or handling of third-party library types (like Pydantic, Attrs, etc.) from the TUI and main application loop. These should be handled by the `hooks/` system via a unified interface.
- **Unified Interface:** Refine the `Inspector` and `Hook` interfaces to allow the TUI to interact with any object type through a consistent, abstracted layer.
- **Enforce Boundaries:** Use `tach` to define and enforce strict architectural boundaries between `core`, `tui`, and `hooks`.

## Acceptance Criteria
- `tach check` passes with the new boundaries enforced.
- The TUI does not import anything from `sus_inspector.hooks.*` except for registration/initialization purposes (if necessary).
- No library-specific code (e.g., `isinstance(obj, pydantic.BaseModel)`) exists outside of `sus_inspector/hooks/`.
- All existing tests pass.
- At least 95% test coverage is maintained.

## Out of Scope
- Adding new features or inspectors.
- Changing the visual design of the TUI.
