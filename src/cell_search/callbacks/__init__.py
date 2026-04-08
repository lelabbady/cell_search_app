"""Dash callback registration package for cell_search."""

from cell_search.callbacks.navigation import register_navigation_callbacks
from cell_search.callbacks.search import register_search_callbacks


def register_callbacks(
    app,
    *,
    umap_data,
    default_scatter_fig,
    default_neighbor_fig,
    utils_module,
    logger,
) -> None:
    """Register all app callbacks while preserving callback IDs/contracts."""
    register_search_callbacks(
        app,
        umap_data=umap_data,
        default_scatter_fig=default_scatter_fig,
        default_neighbor_fig=default_neighbor_fig,
        utils_module=utils_module,
        logger=logger,
    )
    register_navigation_callbacks(
        app,
        umap_data=umap_data,
        utils_module=utils_module,
    )
