"""Command-line entrypoint for launching the standalone cell_search app."""

from __future__ import annotations

from cell_search.app import create_dash_app
from cell_search.config import DEFAULT_HOST, DEFAULT_PORT


def main() -> None:
    """Start the standalone Dash application."""
    app = create_dash_app()
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT, debug=True)


if __name__ == "__main__":
    main()
