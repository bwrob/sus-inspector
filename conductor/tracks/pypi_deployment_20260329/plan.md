# Implementation Plan: PyPI Deployment (pypi_deployment_20260329)

## Phase 1: Preparation & Configuration
- [ ] Task: **Verify `pyproject.toml` metadata**.
    - [ ] Ensure all required fields for PyPI are present (name, version, authors, description, readme, requires-python).
    - [ ] Check classifiers and keywords (optional but recommended).
- [ ] Task: **Build verification**.
    - [ ] Manually test build using `uv build` to ensure artifacts are correct.
    - [ ] Verify that `dist/` contains valid `.tar.gz` and `.whl` files.
- [ ] Task: **PyPI/TestPyPI Trusted Publishing Setup**.
    - [ ] Document the required steps to enable OIDC for the `sus-inspector` repository on PyPI and TestPyPI.

## Phase 2: GitHub Actions Implementation
- [ ] Task: **Create `.github/workflows/publish.yml`**.
    - [ ] Define jobs for building artifacts using `uv`.
    - [ ] Implement job for publishing to **TestPyPI** on push to `main` or manual `workflow_dispatch`.
    - [ ] Implement job for publishing to **PyPI** on new GitHub releases or version tags (`v*`).
- [ ] Task: **Configure OIDC permissions**.
    - [ ] Ensure the workflow has `permissions: id-token: write` and `contents: read`.
- [ ] Task: **Verify workflow syntax**.
    - [ ] Use `action-validator` or equivalent to ensure the YAML is correct.

## Phase 3: Final Verification & Checkpointing
- [ ] Task: **Deployment to TestPyPI**.
    - [ ] Trigger the manual workflow to deploy to TestPyPI.
    - [ ] Verify the package is successfully uploaded and installable via `pip install --index-url https://test.pypi.org/simple/ sus-inspector`.
- [ ] Task: **Conductor - User Manual Verification 'Phase 3: Final Verification & Checkpointing' (Protocol in workflow.md)**.
    - [ ] Self-Review: Confirm the implementation matches the `spec.md`.
    - [ ] Demonstrate: Show the successful TestPyPI deployment status.
    - [ ] Confirm: Obtain final user approval.

---

*Note: Deployment to PyPI will occur upon the first official release tag.*
