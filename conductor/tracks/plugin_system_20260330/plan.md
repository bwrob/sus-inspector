# Implementation Plan: Custom Plugin System

## Phase 1: Preparation & Plugin Loader
- [ ] Task: Implement `load_plugin(path: Path)` using `importlib.util`.
- [ ] Task: Define the `SusPlugin` protocol (with `register()` method).
- [ ] Task: Write tests for loading and executing plugin registration.
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: CLI & Integration
- [ ] Task: Add `--plugin` CLI argument support using `click`.
- [ ] Task: Implement the `register_sus_plugin()` entry point in plugins.
- [ ] Task: Write CLI tests for plugin loading.
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Runtime Registration API
- [ ] Task: Create a high-level `sus_inspector.plugins.register()` function for scripts.
- [ ] Task: Verify registration from an external script (e.g., a sample script).
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Final Polish
- [ ] Task: Add support for custom CSS themes from plugins.
- [ ] Task: Final code quality check.
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)
