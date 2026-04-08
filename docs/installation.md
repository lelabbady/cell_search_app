# Installation

## Requirements

1. Python 3.10 or newer
2. Access to the cell embedding parquet file
3. Optional CAVE token for neuroglancer and CAVE-backed lookups

## Install from PyPI

```bash
pip install cell_search
```

## Install from source (development)

```bash
uv sync
```

## Verify installation

```bash
python -c "import cell_search; print(cell_search.__version__)"
```

## Data file setup

Set CELL_SEARCH_DATA_PATH to the parquet file used by your team.

```bash
export CELL_SEARCH_DATA_PATH=/absolute/path/to/microns_SomaData_AllCells_v661.parquet
```

## Docker

```bash
export CAVE_TOKEN=<your-token>
docker compose up --build
```

Open http://localhost:8050 after startup.
