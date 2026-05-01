# Specification: Comprehensive Test Suite Improvement

## Overview
Improve the `sus-inspector` test suite by focusing on behavioral verification rather than implementation details. Increase overall test coverage to 98% and introduce property-based testing to ensure robustness.

## Functional Requirements
- **Behavioral Testing:** Transition from testing internal state to testing public APIs and TUI behaviors (user flows) using Textual's testing utilities.
- **Comprehensive Coverage:** Exercise all paths in `core.py`, `tui/`, and `hooks/`, reaching at least 98% total coverage.
- **Property-Based Testing:** Implement `hypothesis` tests for core object inspection logic (e.g., in `core.py`) to handle diverse and complex object structures.
- **Integration Verification:** Expand integration tests for third-party libraries (Pydantic, attrs, msgspec) to ensure compatibility across various object configurations.

## Acceptance Criteria
- Overall project test coverage (reported by `pytest-cov`) is ≥ 98%.
- New tests focus on "behavior" (what the system does) rather than "implementation" (how it does it).
- `hypothesis` is successfully integrated and providing value in core inspection logic tests.
- All tests pass in the CI environment (GitHub Actions).

## Out of Scope
- Performance benchmarking tests.
- Significant refactoring of production code (unless strictly required for testability).
