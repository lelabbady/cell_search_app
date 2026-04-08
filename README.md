# Cell Search

A Python package for finding similar cells in embedding space and launching an interactive Dash interface for exploration.

## Installation

### From PyPI

```bash
pip install cell_search
```

### From Source (development)

This repository uses uv for dependency management and poe for tasks.

```bash
uv sync
```

## Quick Start

1. Set environment variables (see .env.example for a template).
2. Run the standalone app.
3. Open http://localhost:8050.

```bash
export CELL_SEARCH_DATA_PATH=/absolute/path/to/microns_SomaData_AllCells_v661.parquet
export CAVE_TOKEN=<your-token>
cell-search
```

For a full onboarding guide, see documentation pages:

1. docs/installation.md
2. docs/quickstart.md
3. docs/configuration.md
4. docs/authentication.md
5. docs/troubleshooting.md

## Run Modes

This package supports two execution modes:

1. Standalone cell_search app (this repository owns runtime and Docker).
2. Embedded app inside dash_on_flask (cell_search imported as a package app factory).

Both modes are supported by the app factory in `src/cell_search/app.py`:

1. `create_dash_app(data_path=None)` for standalone usage.
2. `create_app(name, config=None, server=None, ...)` for dash_on_flask-compatible embedding.

## Standalone cell_search (Local)

```bash
# Optional: set custom parquet path
export CELL_SEARCH_DATA_PATH=/absolute/path/to/microns_SomaData_AllCells_v661.parquet

# Optional: set CAVE token for CAVE/Neuroglancer operations
export CAVE_TOKEN=<your-token>

# Run standalone app
cell-search
```

Default URL: `http://localhost:8050`

## Standalone cell_search (Docker)

```bash
export CAVE_TOKEN=<your-token>
docker compose up --build
```

Default URL: `http://localhost:8050`

If your data file is not in the repository default location, set:

```bash
export CELL_SEARCH_DATA_PATH=/absolute/path/to/microns_SomaData_AllCells_v661.parquet
```

before launching Docker.

## Embedded in dash_on_flask (Local POC)

Use this mode when validating integration with a multi-app Flask host.

1. In dash_on_flask, add `cell_search.create_app` into `DASH_DATASTACK_SUPPORT` for the target datastack.
2. Install this package into dash_on_flask environment (editable install recommended for POC):

```bash
pip install -e /path/to/cell_search_app
```

3. Provide runtime environment in dash_on_flask:

```bash
export CELL_SEARCH_DATA_PATH=/data/microns_SomaData_AllCells_v661.parquet
export CAVE_TOKEN=<your-token>
```

4. Launch dash_on_flask and visit:

`/dash/datastack/<datastack>/apps/cell_search/`

For local proof-of-concept environments using middle_auth_client, `AUTH_DISABLED=true` is often used.

## Development

### Setup

```bash
uv sync
```

### Jupyter

```bash
poe lab
```

### Running Tests

```bash
poe test
```

### Building Documentation

```bash
poe doc-preview
```

### Versioning

```bash
# Dry run to see what will change
poe drybump patch

# Actually bump the version
poe bump patch  # or minor, or major
```



## Profiling

```bash
# Profile with scalene (CPU + memory)
poe profile-all <your script>

# Profile with pyinstrument (CPU only, nicer output)
poe profile <your script>
```

## License

MIT License - see LICENSE file for details.
