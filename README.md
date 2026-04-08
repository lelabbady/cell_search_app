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

## Deployment

This package can run as a standalone local app, in Docker, or embedded in a Flask host application.

## Execution Modes

This package supports three execution modes via the app factory in `src/cell_search/app.py`:

1. **Standalone (local)**: `create_dash_app(data_path=None)` launched by `scripts/Cell_Search_App.py`.
2. **Docker deployment**: `create_dash_app(data_path=None)` launched in a containerized environment.
3. **Embedded in dash_on_flask**: `create_app(name, config=None, server=None, ...)` integrates as a registered Dash app within a multi-app Flask host.

## Standalone (Local)

```bash
# Optional: set custom parquet path
export CELL_SEARCH_DATA_PATH=/absolute/path/to/microns_SomaData_AllCells_v661.parquet

# Optional: set CAVE token for CAVE/Neuroglancer operations
export CAVE_TOKEN=<your-token>

# Run standalone app
uv run python scripts/Cell_Search_App.py
```

Default URL: `http://localhost:8050`

## Docker Deployment

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
2. Install this package into the dash_on_flask environment from PyPI:

```bash
pip install cell_search
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

## License

MIT License - see LICENSE file for details.
