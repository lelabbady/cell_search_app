"""Configuration constants and path resolution for the cell_search app."""

from __future__ import annotations

import os
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent.parent

DATA_PATH_ENV_VAR = "CELL_SEARCH_DATA_PATH"
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "microns_SomaData_AllCells_v661.parquet"

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8050

SOMA_METRICS = [
    "soma_depth_y",
    "nucleus_volume_um",
    "nucleus_area_um",
    "nuclear_area_to_volume_ratio",
    "nuclear_folding_area_um",
    "fraction_nuclear_folding",
    "nucleus_to_soma_ratio",
    "soma_volume_um",
    "soma_area_um",
    "soma_to_nucleus_center_dist",
    "soma_area_to_volume_ratio",
    "soma_synapse_number",
    "soma_synapse_density_um",
]

FEATURE_DICT = {"soma_metrics": SOMA_METRICS}
DEFAULT_FEATURE_SET = "soma_metrics"


def resolve_data_path(explicit_path: str | None = None) -> Path:
    """Resolve the parquet path with stable defaults for local and Docker runs.

    Resolution order:
    1. Explicit function argument
    2. CELL_SEARCH_DATA_PATH environment variable
    3. Repository default data path
    """
    if explicit_path:
        return Path(explicit_path).expanduser().resolve()

    env_value = os.environ.get(DATA_PATH_ENV_VAR)
    if env_value:
        return Path(env_value).expanduser().resolve()

    return DEFAULT_DATA_PATH
