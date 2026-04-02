"""Dash app assembly entrypoints for cell_search."""

from __future__ import annotations

import logging
import os

import dash
import flask
import pandas as pd
import plotly.express as px
from dash import dcc, html

from cell_search import utils
from cell_search.callbacks import register_callbacks
from cell_search.config import resolve_data_path

logger = logging.getLogger(__name__)


def create_dash_app(data_path: str | None = None):
    """Create and return the configured Dash app instance."""
    resolved_data_path = resolve_data_path(data_path)
    logger.info("Loading UMAP data from %s", resolved_data_path)
    umap_data = pd.read_parquet(resolved_data_path)

    if (
        "umap_embedding_x" not in umap_data.columns
        or "umap_embedding_y" not in umap_data.columns
    ):
        raise ValueError(
            "The UMAP data must contain 'umap_embedding_x' and 'umap_embedding_y' columns."
        )

    default_scatter_fig = px.scatter(
        umap_data,
        x="umap_embedding_x",
        y="umap_embedding_y",
        labels={"umap_embedding_x": "UMAP X", "umap_embedding_y": "UMAP Y"},
        color="predicted_subclass",
        template="plotly_white",
        hover_data={
            "predicted_class": True,
            "predicted_subclass": True,
            "nucleus_id": True,
            "umap_embedding_x": False,
            "umap_embedding_y": False,
        },
    )
    default_scatter_fig.update_traces(marker=dict(size=2, opacity=0.4))
    default_scatter_fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)

    default_neighbor_fig = px.scatter(x=[0], y=[0])
    default_neighbor_fig.update_traces(marker=dict(size=2, opacity=0.0))
    default_neighbor_fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)

    app = dash.Dash(__name__, prevent_initial_callbacks=True)

    @app.server.before_request
    def set_auth_token():
        """Inject request-scoped auth token so make_client reads flask.g like deployed apps."""
        flask.g.auth_token = os.environ.get("CAVE_TOKEN")

    app.css.append_css({"external_url": "/assets/dash_style.css"})
    app.title = "Cell Search App"

    app.layout = html.Div(
        style={"display": "flex", "flexDirection": "column", "height": "100vh"},
        children=[
            html.Div(
                style={
                    "textAlign": "center",
                    "padding": "20px",
                    "borderBottom": "1px solid #ccc",
                    "width": "100%",
                },
                children=[
                    html.H1("Cell Search App"),
                    html.H3(
                        "Looking for more cells? This app helps you find other cells in the MICrONS dataset that have similar perisomatic features to your cell of interest."
                    ),
                ],
            ),
            html.Div(
                style={"display": "flex", "height": "300vh"},
                children=[
                    html.Div(
                        style={
                            "flex": "1",
                            "padding": "20px",
                            "borderRight": "1px solid #ccc",
                        },
                        children=[
                            html.H4("1. What cell are you interested in?"),
                            html.P(
                                "Enter the cell ID and select the type of ID you have."
                            ),
                            dcc.Input(
                                id="cell-id-input",
                                type="text",
                                placeholder="Enter Cell ID",
                                style={"width": "100%", "marginBottom": "10px"},
                            ),
                            dcc.Dropdown(
                                id="id-type-dropdown",
                                options=[
                                    {"label": "Nucleus ID", "value": "nucleus_id"},
                                    {"label": "Segment ID", "value": "seg_id"},
                                ],
                                placeholder="Select ID Type",
                                style={"width": "100%"},
                            ),
                            html.Button(
                                "Find My Cell",
                                id="search-button",
                                style={"width": "50%", "marginTop": "10px"},
                            ),
                            html.Button(
                                "Reset",
                                id="reset-button",
                                style={"width": "30%", "marginTop": "10px"},
                            ),
                            html.H4("2. How many similar cells would you like to see?"),
                            dcc.Input(
                                id="neighbor-id-input",
                                type="text",
                                placeholder="Enter the number of similar cells you would like to search for",
                                style={"width": "100%", "marginBottom": "10px"},
                            ),
                            html.Button(
                                "Find More Cells!",
                                id="neighbor-button",
                                style={"width": "33%", "marginTop": "10px"},
                            ),
                            html.Button(
                                "Copy Cell IDs",
                                id="copy-button",
                                style={"width": "33%", "marginTop": "10px"},
                            ),
                            html.Button(
                                "Open Neuroglancer",
                                id="neuroglancer-link-button",
                                style={"width": "33%", "marginTop": "10px"},
                            ),
                            dcc.Store(id="copy-text-store"),
                            dcc.Store(id="neuroglancer-url-store"),
                            html.Div(id="copy-trigger", style={"display": "none"}),
                            html.Div(
                                id="neuroglancer-open-trigger",
                                style={"display": "none"},
                            ),
                            dcc.Graph(
                                figure=default_neighbor_fig,
                                id="default-neighbor-plot",
                                style={"display": "none"},
                            ),
                        ],
                    ),
                    html.Div(
                        style={
                            "height": "500px",
                            "width": "400px",
                            "flex": "2",
                            "padding": "20px",
                        },
                        children=[
                            html.H4("Interactive UMAP with predicted cell-types"),
                            dcc.Graph(
                                figure=default_scatter_fig, id="default-scatter-plot"
                            ),
                            html.Div(id="output-content", style={"marginTop": "20px"}),
                        ],
                    ),
                ],
            ),
        ],
    )

    register_callbacks(
        app,
        umap_data=umap_data,
        default_scatter_fig=default_scatter_fig,
        default_neighbor_fig=default_neighbor_fig,
        utils_module=utils,
        logger=logger,
    )

    return app


def get_dash_app():
    """Backward-compatible alias for obtaining a built Dash app instance."""
    return create_dash_app()
