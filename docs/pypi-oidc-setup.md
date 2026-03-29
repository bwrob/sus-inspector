# Trusted Publishing (OIDC) Setup for PyPI

This project uses **Trusted Publishing (OIDC)** to securely deploy to PyPI and TestPyPI without managing long-lived API tokens.

## 1. TestPyPI Setup

1.  Log in to [test.pypi.org](https://test.pypi.org/).
2.  Go to **Publishing** in your account settings.
3.  Add a new **GitHub Publisher**:
    -   **Owner**: `bwrob`
    -   **Repository**: `sus-inspector`
    -   **Workflow Name**: `publish.yml`
    -   **Environment**: `testpypi` (optional, but recommended if using environment-specific protection)

## 2. PyPI Setup

1.  Log in to [pypi.org](https://pypi.org/).
2.  Go to **Publishing** in your account settings.
3.  Add a new **GitHub Publisher**:
    -   **Owner**: `bwrob`
    -   **Repository**: `sus-inspector`
    -   **Workflow Name**: `publish.yml`
    -   **Environment**: `pypi`

## 3. GitHub Actions Workflow

The workflow must have the following permissions to request the OIDC token:

```yaml
permissions:
  id-token: write # Mandatory for OIDC
  contents: read  # Required to check out code
```

The publishing job should use the following actions:
-   `pypa/gh-action-pypi-publish@release/v1`
