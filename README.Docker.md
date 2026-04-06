### Standalone cell_search container

This repository's Docker setup runs the standalone cell_search app.

Start it with:

`docker compose up --build`

Your application will be available at http://localhost:8050.

If needed, set these environment variables before launch:

1. `CAVE_TOKEN` for CAVE-backed features.
2. `CELL_SEARCH_DATA_PATH` to override the default parquet file path.

### Embedded mode in dash_on_flask

For multi-app hosting, this package is intended to be installed into a dash_on_flask environment and registered via `cell_search.create_app(...)` in the dash_on_flask app config. In that mode, container ownership and startup are managed by dash_on_flask rather than this repository's compose file.

### Deploying your application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)