"""Search and neighbor callbacks for the cell search app."""

from __future__ import annotations

import dash
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output


def register_search_callbacks(
    app,
    *,
    umap_data,
    default_scatter_fig,
    default_neighbor_fig,
    utils_module,
    logger,
) -> None:
    """Register search/highlight and neighbor/copy callbacks."""

    @app.callback(
        [
            Output("default-scatter-plot", "figure"),
            Output("default-neighbor-plot", "figure"),
            Output("default-neighbor-plot", "style"),
        ],
        [Input("search-button", "n_clicks"), Input("reset-button", "n_clicks")],
        [
            dash.dependencies.State("cell-id-input", "value"),
            dash.dependencies.State("id-type-dropdown", "value"),
        ],
    )
    def highlight_cell(search_clicks, reset_clicks, cell_id, id_type):
        ctx = dash.callback_context
        if not ctx.triggered:
            return default_scatter_fig, default_neighbor_fig, {"display": "none"}

        if id_type == "seg_id":
            cell_id = utils_module.get_nuc_id_from_seg_id(cell_id)

        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if triggered_id == "reset-button":
            return default_scatter_fig, default_neighbor_fig, {"display": "none"}

        if triggered_id == "search-button" and cell_id:
            plot_data = umap_data.copy()
            cell_id = int(cell_id)

            plot_data["marker_size"] = 2
            plot_data["marker_color"] = "lightgray"
            plot_data["marker_opacity"] = 0.4

            plot_data.loc[plot_data["nucleus_id"] == cell_id, "marker_size"] = 10
            plot_data.loc[plot_data["nucleus_id"] == cell_id, "marker_color"] = "orange"
            plot_data.loc[plot_data["nucleus_id"] == cell_id, "marker_opacity"] = 1.0
            logger.info(
                "cell predicted_subclass: %s",
                plot_data.loc[
                    plot_data["nucleus_id"] == cell_id
                ].predicted_subclass.values[0],
            )
            plot_data = plot_data.sort_values(by="marker_size", ascending=True)

            scatter_fig = px.scatter(
                plot_data,
                x="umap_embedding_x",
                y="umap_embedding_y",
                title="Cell of Interest within the Dataset",
                labels={"umap_embedding_x": "UMAP X", "umap_embedding_y": "UMAP Y"},
                template="plotly_white",
                hover_data={
                    "predicted_class": True,
                    "predicted_subclass": True,
                    "nucleus_id": True,
                    "umap_embedding_x": False,
                    "umap_embedding_y": False,
                },
            )
            scatter_fig.update_traces(
                marker=dict(
                    size=plot_data["marker_size"],
                    color=plot_data["marker_color"],
                    opacity=plot_data["marker_opacity"],
                    line=dict(width=0),
                )
            )
            scatter_fig.update_layout(
                height=600, xaxis_showgrid=False, yaxis_showgrid=False
            )

            return scatter_fig, default_neighbor_fig, {"display": "none"}

        return default_scatter_fig, default_neighbor_fig, {"display": "none"}

    @app.callback(
        Output("default-scatter-plot", "figure", allow_duplicate=True),
        Output("default-neighbor-plot", "figure", allow_duplicate=True),
        Output(
            component_id="default-neighbor-plot",
            component_property="style",
            allow_duplicate=True,
        ),
        Output("copy-text-store", "data"),
        [Input("neighbor-button", "n_clicks"), Input("copy-button", "n_clicks")],
        [
            dash.dependencies.State("cell-id-input", "value"),
            dash.dependencies.State("neighbor-id-input", "value"),
            dash.dependencies.State("id-type-dropdown", "value"),
        ],
        prevent_initial_call=True,
    )
    def handle_neighbor_and_copy(
        neighbor_clicks, copy_clicks, cell_id, n_neighbors, id_type
    ):
        ctx = dash.callback_context
        if not ctx.triggered:
            return (
                default_scatter_fig,
                default_neighbor_fig,
                {"display": "none"},
                dash.no_update,
            )

        if id_type == "seg_id":
            cell_id = utils_module.get_nuc_id_from_seg_id(cell_id)

        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if (
            triggered_id == "neighbor-button"
            and neighbor_clicks
            and n_neighbors
            and n_neighbors.isdigit()
        ):
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
            cell_id = nuc_neighbors[0]
            nuc_neighbors = nuc_neighbors[1:]

            plot_data["marker_size"] = 2
            plot_data["marker_color"] = "lightgray"
            plot_data["marker_opacity"] = 0.4

            plot_data.loc[plot_data.nucleus_id.isin(nuc_neighbors), "marker_size"] = 5
            plot_data.loc[plot_data.nucleus_id.isin(nuc_neighbors), "marker_color"] = (
                "teal"
            )
            plot_data.loc[
                plot_data.nucleus_id.isin(nuc_neighbors), "marker_opacity"
            ] = 1.0

            plot_data.loc[plot_data["nucleus_id"] == cell_id, "marker_size"] = 10
            plot_data.loc[plot_data["nucleus_id"] == cell_id, "marker_color"] = "orange"
            plot_data.loc[plot_data["nucleus_id"] == cell_id, "marker_opacity"] = 1.0

            plot_data = plot_data.sort_values(by="marker_size", ascending=True)
            scatter_fig = px.scatter(
                plot_data,
                x="umap_embedding_x",
                y="umap_embedding_y",
                title=f"{len(nuc_neighbors)} Nearest Neighbors to your Cell of Interest",
                labels={"umap_embedding_x": "UMAP X", "umap_embedding_y": "UMAP Y"},
                template="plotly_white",
                hover_data={
                    "predicted_class": True,
                    "predicted_subclass": True,
                    "nucleus_id": True,
                    "umap_embedding_x": False,
                    "umap_embedding_y": False,
                },
            )
            scatter_fig.update_traces(
                marker=dict(
                    size=plot_data["marker_size"],
                    color=plot_data["marker_color"],
                    opacity=plot_data["marker_opacity"],
                    line=dict(width=0),
                )
            )
            scatter_fig.update_layout(
                height=500, xaxis_showgrid=False, yaxis_showgrid=False
            )

            left = len(all_distances) - n_neighbors - 1
            neighbor_colors = (
                ["orange"] + (["teal"] * n_neighbors) + (["lightgray"] * left)
            )
            neighbor_distance_fig = px.scatter(
                x=np.arange(len(all_distances)),
                y=all_distances,
                title="Distance to Nearest Neighbors",
                labels={"x": "Neighbor Index", "y": "Distance"},
                template="plotly_white",
                log_x=True,
                log_y=True,
            )

            neighbor_distance_fig.update_layout(
                height=300,
                width=500,
                xaxis_showgrid=False,
                yaxis_showgrid=False,
            )
            neighbor_distance_fig.update_traces(marker=dict(color=neighbor_colors))

            visibility = {"display": "block"}
            return scatter_fig, neighbor_distance_fig, visibility, dash.no_update

        if (
            triggered_id == "copy-button"
            and copy_clicks
            and n_neighbors
            and n_neighbors.isdigit()
        ):
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
            return (
                dash.no_update,
                dash.no_update,
                dash.no_update,
                ", ".join(map(str, seg_ids)),
            )

        visibility = {"display": "none"}
        return default_scatter_fig, default_neighbor_fig, visibility, dash.no_update

    app.clientside_callback(
        """
        async function(text) {
            if (!text || typeof text !== 'string' || text.length === 0) {
                return window.dash_clientside.no_update;
            }
            try {
                if (navigator && navigator.clipboard && navigator.clipboard.writeText) {
                    await navigator.clipboard.writeText(text);
                } else {
                    const temp = document.createElement('textarea');
                    temp.value = text;
                    document.body.appendChild(temp);
                    temp.select();
                    document.execCommand('copy');
                    document.body.removeChild(temp);
                }
            } catch (e) {
                console.warn('Clipboard copy failed:', e);
            }
            return '';
        }
        """,
        Output("copy-trigger", "children"),
        Input("copy-text-store", "data"),
        prevent_initial_call=True,
    )
