# Specification: Type Safety Refactor (basedpyright & ty)

## Overview
This track involves improving the type safety of the `sus-inspector` project by resolving all existing `basedpyright` errors in the core library and test suite. We will also adjust the `basedpyright` configuration to disable the `reportAny` check, acknowledging that `Any` is sometimes necessary when dealing with dynamic object introspection.

## Functional Requirements
- **basedpyright Configuration:** Update `pyrightconfig.json` to disable the `reportAny` check.
- **Type Fixing (Core):** Systematically resolve all typing errors reported by `basedpyright` within the `src/sus_inspector` directory.
- **Type Fixing (Tests):** Systematically resolve all typing errors reported by `basedpyright` within the `tests/` directory.
- **`ty` Integration:** Ensure that `ty` tasks and related configurations are functioning correctly with the updated types.

## Non-Functional Requirements
- **Zero Errors:** After completion, running `basedpyright` should result in zero reported errors (excluding `reportAny`).
- **Maintainability:** Use clear and accurate type hints that improve code readability and developer experience.
- **Performance:** Ensure that type checking remains fast and efficient.

## Acceptance Criteria
- [ ] `pyrightconfig.json` is updated to disable `reportAny`.
- [ ] Running `basedpyright` on `src/` results in zero errors.
- [ ] Running `basedpyright` on `tests/` results in zero errors.
- [ ] All `ty` tasks (e.g., `ty test`, `ty lint`) run successfully without type-related issues.

## Out of Scope
- **Strict `Any` Removal:** Complete removal of all `Any` types from the codebase.
- **New Feature Development:** This track is strictly focused on type safety and refactoring.
- **Full Library Typing:** Typing for 100% of all external dependencies (if untyped).
