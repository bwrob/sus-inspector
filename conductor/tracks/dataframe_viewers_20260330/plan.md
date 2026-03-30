# Implementation Plan: Custom Data Viewers

## Phase 1: Foundation & Base Classes
- [ ] Task: Create `src/sus_inspector/hooks/dataframe.py` with `BaseDataFrameInspector`.
- [ ] Task: Implement shared logic for pagination (truncation/chunking), shape extraction, and memory footprint calculation.
- [ ] Task: Implement a standardized `render_table` method using Rich `Table` with consistent styling.
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Pandas Implementation
- [ ] Task: Implement `PandasInspector` to handle `pandas.DataFrame` and `pandas.Series`.
- [ ] Task: Implement TDD tests in `tests/test_hooks_pandas.py`.
- [ ] Task: Register `PandasInspector` in `src/sus_inspector/hooks/registry.py` (lazy-loading).
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Numpy Implementation
- [ ] Task: Implement `NumpyInspector` to handle `numpy.ndarray`.
- [ ] Task: Implement TDD tests in `tests/test_hooks_numpy.py`.
- [ ] Task: Register `NumpyInspector` in `src/sus_inspector/hooks/registry.py` (lazy-loading).
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Polars Implementation
- [ ] Task: Implement `PolarsInspector` to handle `polars.DataFrame` and `polars.Series`.
- [ ] Task: Implement TDD tests in `tests/test_hooks_polars.py`.
- [ ] Task: Register `PolarsInspector` in `src/sus_inspector/hooks/registry.py` (lazy-loading).
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

## Phase 5: Refinement & Final Checks
- [ ] Task: Ensure visual consistency (headers, indices, alignment) across all data viewers.
- [ ] Task: Optimize for performance with extremely large datasets (lazy access).
- [ ] Task: Final code quality check using `rtk poe code-quality`.
- [ ] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)
