# Implementation Plan: Architectural Review and Decoupling

## Phase 1: Architectural Boundaries
- [ ] Task: Define boundaries in `tach.toml`.
- [ ] Task: Run `tach check` and identify existing violations.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Architectural Boundaries' (Protocol in workflow.md)

## Phase 2: Core Interface Abstraction
- [ ] Task: Refine `Inspector` and `Hook` interfaces in `sus_inspector/hooks/base.py` and `registry.py`.
- [ ] Task: Update all existing hooks to adhere to the refined interfaces.
- [ ] Task: Write tests verifying the unified interface across different object types.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Core Interface Abstraction' (Protocol in workflow.md)

## Phase 3: TUI Decoupling
- [ ] Task: Audit `sus_inspector/tui/app.py` and `widgets.py` for library-specific references (Pydantic, etc.).
- [ ] Task: Refactor TUI components to use only the abstracted `Inspector` registry and interfaces.
- [ ] Task: Verify that `tach check` passes for the TUI module.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: TUI Decoupling' (Protocol in workflow.md)

## Phase 4: Final Verification and Cleanup
- [ ] Task: Perform a final audit of `cli.py` and `main.py` for unnecessary coupling.
- [ ] Task: Ensure all tests pass and coverage is >= 95%.
- [ ] Task: Run `uv run poe code-quality` and fix all issues.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Final Verification and Cleanup' (Protocol in workflow.md)
