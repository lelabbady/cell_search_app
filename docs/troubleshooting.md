# Troubleshooting

## App does not start

1. Verify CELL_SEARCH_DATA_PATH points to an existing parquet file.
2. Verify Python environment has installed dependencies.
3. Check port conflicts on 8050.

## Missing or failed neuroglancer/CAVE lookups

1. Verify CAVE_TOKEN is set and valid.
2. Verify CELL_SEARCH_DATASTACK and CAVE_SERVER_ADDRESS values.
3. In embedded mode, verify host app provides flask.g.auth_token.

## Tests fail unexpectedly

Run tests through uv to avoid stale local pytest launcher paths.

```bash
uv run python -m pytest --cov=cell_search tests
```

## Docker issues

1. Confirm environment variables are exported before docker compose up.
2. Confirm mounted data path is available inside the container.
