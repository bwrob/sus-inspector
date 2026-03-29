# Specification: Collapsible Class Information Pane with Double Registry

## Overview
This track involves implementing a collapsible pane in the `sus-inspector` TUI to display class-level metadata for the inspected object. The pane will be hidden by default and can be toggled using the 'c' key. It will be positioned above or below the main instance view (Stacked Layout). Crucially, a "Double Registry" system will be implemented to allow for class-specific customization of both instance and class-level information.

## Functional Requirements
- **Double Registry System:**
    - **Instance Registry:** Mappings for rendering instance-level information.
    - **Class Registry:** Mappings for rendering class-level information.
    - Both registries must provide default implementations.
    - A single class may have a custom implementation in one registry but use the default in the other.
- **Collapsible UI Component:** A new UI pane that can be shown or hidden.
- **Default State:** The class information pane must be collapsed (hidden) by default.
- **'c' Keyboard Shortcut:** Pressing 'c' will toggle the visibility of the class pane.
- **Stacked Layout:** The pane should appear stacked (horizontal) relative to the instance view.
- **Content Rendering (Default):** The class pane must display:
    - **Docstrings:** The class's `__doc__` string.
    - **Class Fields:** Attributes defined at the class level.
    - **Class Methods:** Methods decorated with `@classmethod`.
    - **Inheritance:** Method Resolution Order (MRO) and direct base classes.
    - **Inheritance Tree:** A visual representation of the class hierarchy.
- **Visual Styling:** The pane should have a distinct colored border.

## Non-Functional Requirements
- **Extensibility:** The double registry system must be designed for easy extension via hooks or direct registration.
- **Performance:** Ensure that registry lookups and metadata extraction do not impact the UI's responsiveness.

## Acceptance Criteria
- [ ] A class can have a custom instance view and a default class view.
- [ ] A class can have a custom class view and a default instance view.
- [ ] Pressing 'c' toggles the class information pane correctly.
- [ ] The class information pane displays the correct metadata for various object types.
- [ ] The pane layout is horizontal (stacked).
- [ ] The pane has a distinct visual appearance (colored border).

## Out of Scope
- **Interactive Inheritance Tree:** Navigating the inheritance tree directly.
- **Side-by-Side Layout:** Only the horizontal stacked layout is required for now.
