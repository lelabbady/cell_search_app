# Configuration

## Environment Variables

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| CELL_SEARCH_DATA_PATH | Yes | ./data/microns_SomaData_AllCells_v661.parquet | Parquet file for embedding/search data |
| CAVE_TOKEN | Recommended | unset | Authentication token used for CAVE and neuroglancer operations |
| CELL_SEARCH_DATASTACK | No | minnie65_public | Datastack for CAVE-backed lookups |
| CAVE_SERVER_ADDRESS | No | https://global.daf-apis.com | Base URL for CAVE services |
| CELL_SEARCH_HOST | No | 0.0.0.0 | Host binding for standalone mode |
| CELL_SEARCH_PORT | No | 8050 | Port binding for standalone mode |
| AUTH_DISABLED | No | false | Local smoke-testing only |

## Notes

1. Embedded mode reads auth context from the host Flask app.
2. Standalone mode can use CAVE_TOKEN from the environment.
3. Keep AUTH_DISABLED false in normal team usage.
