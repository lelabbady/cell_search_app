# Quick Start

This path is intended for coworkers who just want to run the app.

## 1. Install

```bash
pip install cell_search
```

## 2. Configure environment

```bash
export CELL_SEARCH_DATA_PATH=/absolute/path/to/microns_SomaData_AllCells_v661.parquet
export CAVE_TOKEN=<your-token>
```

If needed, copy .env.example into your shell environment and update values.

## 3. Run standalone app

```bash
cell-search
```

Open http://localhost:8050.

## 4. Embedded mode (dash_on_flask)

Use cell_search.create_app in the host application and provide CELL_SEARCH_DATA_PATH and CAVE_TOKEN in that runtime environment.
