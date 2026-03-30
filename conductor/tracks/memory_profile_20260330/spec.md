# Specification: Memory Profiling

## Overview
Add a detailed view for memory usage profiling of objects, showing both the object's direct size and its deep, recursive size.

## Functional Requirements
- **Detailed Size Breakdown**: Show the size of the object's `__dict__`, `__slots__`, and the recursive size of all children.
- **Configurable Depth Limit**: A setting (default=3) to limit the depth of the recursive size calculation for performance.
- **Top Contributors List**: Display a list of the 5-10 largest attributes/children in terms of memory.
- **Visual Feedback**: Progress bar or indicator while calculating large, deep sizes.

## Technical Details
- Use `sys.getsizeof()` for base size.
- Implement a custom, safe recursive size calculator that handles circular references.
