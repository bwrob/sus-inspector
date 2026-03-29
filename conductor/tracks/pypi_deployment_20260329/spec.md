# Specification: PyPI Deployment (pypi_deployment_20260329)

## Overview
Automate the publishing of `sus-inspector` to PyPI and TestPyPI using GitHub Actions. This will streamline the release process and ensure that the package is available to the community.

## Functional Requirements
- **GitHub Actions Workflow**: Create a workflow to build and publish the package.
- **Deployment Targets**:
    - **TestPyPI**: For testing the deployment process and package integrity.
    - **PyPI**: For official releases.
- **Triggers**:
    - Deploy to **TestPyPI** on push to `main` or manual trigger.
    - Deploy to **PyPI** when a new GitHub Release is created or a version tag (e.g., `v*`) is pushed.
- **Authentication**: Use **OIDC (Trusted Publishing)** to authenticate with PyPI/TestPyPI, eliminating the need for long-lived secrets.

## Non-Functional Requirements
- **Simplicity**: Maintain manual versioning in `pyproject.toml`. No dynamic versioning or git hashes in the version string.
- **Security**: Follow PyPI best practices for Trusted Publishing.

## Acceptance Criteria
- [ ] GitHub Action successfully builds the wheel and source distribution using `uv`.
- [ ] Successful deployment to TestPyPI can be triggered manually.
- [ ] Creating a release/tag triggers a successful deployment to PyPI.
- [ ] No manual secrets (like `PYPI_API_TOKEN`) are required in GitHub settings.

## Out of Scope
- Automated changelog generation.
- Automatic version bumping (remains manual).
