"""Cell search package for embedding-based similar-cell workflows."""

from .app import create_app, create_dash_app, get_dash_app
from .data_access import configure_data_access

__version__ = "0.0.1"

__all__ = [
    "__version__",
    "configure_data_access",
    "create_app",
    "create_dash_app",
    "get_dash_app",
]
