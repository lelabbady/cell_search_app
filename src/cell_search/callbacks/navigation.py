"""Neuroglancer navigation callbacks for the cell search app."""

from __future__ import annotations

import dash
from dash.dependencies import Input, Output


def register_navigation_callbacks(app, *, umap_data, utils_module) -> None:
    """Register neuroglancer server and clientside callbacks."""

    @app.callback(
        Output("neuroglancer-url-store", "data"),
        [Input("neuroglancer-link-button", "n_clicks")],
        [
            dash.dependencies.State("cell-id-input", "value"),
            dash.dependencies.State("neighbor-id-input", "value"),
            dash.dependencies.State("id-type-dropdown", "value"),
        ],
        prevent_initial_call=True,
    )
    def open_neuroglancer(neuroglancer_clicks, cell_id, n_neighbors, id_type):
        ctx = dash.callback_context

        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if triggered_id == "neuroglancer-link-button" and cell_id and n_neighbors:
            if id_type == "seg_id":
                cell_id = utils_module.get_nuc_id_from_seg_id(cell_id)

            n_neighbors = int(n_neighbors)
            plot_data = umap_data.copy()
            nuc_neighbors, soma_neighbors, all_distances = (
                utils_module.find_nearest_neighbors(
                    df=plot_data,
                    cell_id=cell_id,
                    feature_set="soma_metrics",
                    n_neighbors=n_neighbors,
                )
            )
            seg_ids = utils_module.get_latest_seg_ids(nuc_neighbors)

            return utils_module.get_neuroglancer_link(segment_ids=seg_ids)

        if triggered_id == "neuroglancer-link-button":
            return dash.no_update

        return dash.no_update

    app.clientside_callback(
        """
        function(url) {
            if (!url || typeof url !== 'string' || url.length === 0) {
                return window.dash_clientside.no_update;
            }
            window.open(url, '_blank', 'noopener,noreferrer');
            return '';
        }
        """,
        Output("neuroglancer-open-trigger", "children"),
        Input("neuroglancer-url-store", "data"),
        prevent_initial_call=True,
    )
