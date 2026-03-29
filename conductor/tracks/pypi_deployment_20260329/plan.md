# Implementation Plan: PyPI Deployment (pypi_deployment_20260329)

## Phase 1: Preparation & Configuration
- [x] Task: **Verify `pyproject.toml` metadata**.
    - [x] Ensure all required fields for PyPI are present (name, version, authors, description, readme, requires-python).
    - [x] Check classifiers and keywords (optional but recommended).
- [x] Task: **Build verification**.
    - [x] Manually test build using `uv build` to ensure artifacts are correct.
    - [x] Verify that `dist/` contains valid `.tar.gz` and `.whl` files.
- [x] Task: **PyPI/TestPyPI Trusted Publishing Setup**.
    - [x] Document the required steps to enable OIDC for the `sus-inspector` repository on PyPI and TestPyPI.

## Phase 2: GitHub Actions Implementation
- [x] Task: **Create `.github/workflows/publish.yml`**.
    - [x] Define jobs for building artifacts using `uv`.
    - [x] Implement job for publishing to **TestPyPI** on push to `main` or manual `workflow_dispatch`.
    - [x] Implement job for publishing to **PyPI** on new GitHub releases or version tags (`v*`).
- [x] Task: **Configure OIDC permissions**.
    - [x] Ensure the workflow has `permissions: id-token: write` and `contents: read`.
- [x] Task: **Verify workflow syntax**.
    - [x] Use `action-validator` or equivalent to ensure the YAML is correct.

## Phase 3: Final Verification & Checkpointing
- [x] Task: **Deployment to TestPyPI**.
    - [x] Trigger the manual workflow to deploy to TestPyPI.
    - [x] Verify the package is successfully uploaded and installable via `pip install --index-url https://test.pypi.org/simple/ sus-inspector`.
- [x] Task: **Conductor - User Manual Verification 'Phase 3: Final Verification & Checkpointing' (Protocol in workflow.md)**.
    - [x] Self-Review: Confirm the implementation matches the `spec.md`.
    - [x] Demonstrate: Show the successful TestPyPI deployment status.
    - [x] Confirm: Obtain final user approval.

---

*Note: Deployment to PyPI will occur upon the first official release tag.*
