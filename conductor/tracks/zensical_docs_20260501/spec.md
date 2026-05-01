# Specification: Documentation Migration and Enhancement (Zensical)

## Overview
Migrate the `sus-inspector` documentation from MkDocs to Zensical. The goal is to modernize the documentation site, align its visual style with the user's Quarto blog (bwrob.github.io), and integrate rich, interactive visual snapshots of the TUI.

## Functional Requirements
- **Migration:** Convert existing Markdown documentation from MkDocs format to Zensical.
- **Visual Alignment:** Customize the Zensical theme (CSS/Templates) to match the aesthetics of `bwrob.github.io`.
- **Rich Media Integration:**
    - **Static Snapshots:** Use `Rich` to generate and embed high-quality SVG snapshots of object inspection results.
    - **Interactive Demos:** Integrate `asciinema` or SVG-based terminal recordings to demonstrate TUI navigation.
    - **Automated Snapshots:** Implement a system using Textual's `Pilot` to automatically capture TUI states for documentation during the CI build.
- **Expanded Content:** Add "In-Depth" sections with complex examples and detailed explanations of the `hooks` system.

## Acceptance Criteria
- Zensical site is fully operational and replaces the MkDocs site.
- The site design closely follows the style of `bwrob.github.io`.
- Snapshots and demos are correctly rendered in the live documentation.
- `mkdocs.yml` and related MkDocs dependencies are removed.

## Out of Scope
- Rewriting core library code.
- Implementing a full search engine if Zensical doesn't provide one out-of-the-box (to be evaluated).
- Hosting the site (limited to local build/verification).
