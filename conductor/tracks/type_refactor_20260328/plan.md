# Implementation Plan: Type Safety Refactor (basedpyright & ty)

## Phase 1: Configuration & Initial Audit
- [ ] Task: Update `basedpyright` configuration.
    - [ ] Create a feature branch `feat/typing-config-update`.
    - [ ] Modify `pyrightconfig.json` to include `"reportAny": false`.
    - [ ] Verify the change by running `basedpyright` and checking the output.
- [ ] Task: Audit the codebase for existing typing issues.
    - [ ] Run `basedpyright src/` and `basedpyright tests/` to generate a list of all errors.
    - [ ] Categorize the errors to identify common patterns or problematic areas.
- [ ] Task: Conductor - User Manual Verification 'Configuration & Initial Audit' (Protocol in workflow.md)

## Phase 2: Core Library Typing Refactor
- [ ] Task: Resolve typing errors in `src/sus_inspector/core.py` and `src/sus_inspector/instances.py`.
    - [ ] Create a feature branch `feat/typing-refactor-core`.
    - [ ] Apply accurate type hints to classes, methods, and functions.
    - [ ] Use `TypedDict`, `Protocol`, or `TypeVar` as needed to improve accuracy.
    - [ ] Verify each fix by re-running `basedpyright`.
- [ ] Task: Resolve typing errors in remaining files in `src/sus_inspector/`.
    - [ ] Create a feature branch `feat/typing-refactor-remaining`.
    - [ ] Apply fixes to `cli.py`, `main.py`, `hooks/`, and `tui/`.
    - [ ] Ensure all internal API boundaries are correctly typed.
    - [ ] Verify each fix by re-running `basedpyright`.
- [ ] Task: Conductor - User Manual Verification 'Core Library Typing Refactor' (Protocol in workflow.md)

## Phase 3: Test Suite Typing Refactor
- [ ] Task: Resolve typing errors in the `tests/` directory.
    - [ ] Create a feature branch `feat/typing-refactor-tests`.
    - [ ] Apply fixes to test functions, fixtures, and mock objects.
    - [ ] Ensure tests are correctly typed to prevent regressions.
    - [ ] Verify each fix by re-running `basedpyright`.
- [ ] Task: Verify `ty` integration.
    - [ ] Run `ty test` and `ty lint` (if applicable) to confirm no issues.
    - [ ] Resolve any remaining type-related issues in `ty` tasks or configuration.
- [ ] Task: Conductor - User Manual Verification 'Test Suite Typing Refactor' (Protocol in workflow.md)

## Phase 4: Final Polish & Verification
- [ ] Task: Perform a final global type check.
    - [ ] Run `basedpyright` on the entire project and confirm zero errors (excluding `reportAny`).
    - [ ] Perform a full review for visual consistency and responsiveness.
    - [ ] Ensure all links and images are functioning correctly.
    - [ ] Validate the site's responsiveness on different screen sizes.
- [ ] Task: Conductor - User Manual Verification 'Final Polish & Verification' (Protocol in workflow.md)
