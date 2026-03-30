# Specification: Custom Data Viewers (Pandas, Polars, Numpy)

## Overview
Add custom object-specific rendering logic for `pandas`, `polars`, and `numpy` data structures within the `sus-inspector` TUI. The goal is to provide a consistent, high-performance visual representation of tabular and array data across these popular libraries.

## Functional Requirements
- **Library Support**:
    - **Pandas**: Support for `DataFrame` and `Series`.
    - **Polars**: Support for `DataFrame` and `Series`.
    - **Numpy**: Support for `ndarray`.
- **Standardized Table Layout**:
    - Consistent visual style across all viewers, including headers, indices, and borders.
    - Right-aligned numeric data and left-aligned text/string data.
- **Data Type Indicators**:
    - Display the data type (`dtype`) for each column in DataFrames or the entire structure for Series/Arrays.
- **Shape & Size Summary**:
    - Display the dimensions (e.g., `(100, 10)`) and total row/column counts.
    - Show an estimate of the memory footprint.
- **Paginated View (Performance)**:
    - Large datasets must be loaded and displayed in pages/chunks to ensure TUI responsiveness.
    - Default page size should be configurable (e.g., 50-100 rows).
- **Interactive Navigation**:
    - Support for both vertical (rows) and horizontal (columns/axes) scrolling within the active page.

## Non-Functional Requirements
- **Performance**: Lazy-loading of data chunks from the source objects.
- **Visual Consistency**: Unified "look and feel" within the `sus-inspector` theme.
- **Robustness**: Graceful handling of empty or malformed data.

## Acceptance Criteria
- [ ] Inspecting a `pandas.DataFrame` displays a paginated, formatted table.
- [ ] Inspecting a `polars.DataFrame` displays a visually consistent table.
- [ ] Inspecting a `numpy.ndarray` displays its dimensions and formatted data.
- [ ] TUI responsiveness is maintained when inspecting objects with >1,000,000 rows.
- [ ] Shape, dtypes, and memory info are clearly visible.

## Out of Scope
- Interactive data editing (Read-only for now).
- Complex in-TUI sorting, filtering, or querying.
- Support for multi-index or deeply nested hierarchical structures.
