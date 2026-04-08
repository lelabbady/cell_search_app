# Cell Search

Cell Search is a package and app for finding similar cells in embedding space, then exploring results in an interactive interface.

## Start Here

1. Installation: installation.md
2. Quick Start: quickstart.md
3. Configuration: configuration.md
4. Authentication: authentication.md
5. Troubleshooting: troubleshooting.md

## Execution Modes

Cell Search can run in two supported modes:

1. Standalone app from this repository via `scripts/Cell_Search_App.py`.
2. Embedded app imported into a dash_on_flask host via `cell_search.create_app(...)`.

## Refactor Status

The application has been reorganized to align with the dash_connectivity_viewer ecosystem while preserving current behavior.

Use the following pages for implementation details:

1. Architecture: module boundaries and runtime assembly path.
2. Compatibility and Deprecation: temporary wrappers and removal criteria.
3. Reorg Baseline Checklist: parity checks for local and Docker verification.
