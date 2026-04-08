from types import SimpleNamespace

import dash
import pandas as pd
import plotly.express as px

from cell_search.callbacks import register_callbacks


def _build_umap_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "umap_embedding_x": [0.0, 1.0],
            "umap_embedding_y": [0.0, 1.0],
            "predicted_class": ["a", "b"],
            "predicted_subclass": ["x", "y"],
            "nucleus_id": [1, 2],
            "soma_id": [10, 20],
        }
    )


def test_register_callbacks_adds_expected_callback_contracts() -> None:
    app = dash.Dash(__name__, prevent_initial_callbacks=True)
    umap_data = _build_umap_df()

    default_scatter_fig = px.scatter(
        umap_data,
        x="umap_embedding_x",
        y="umap_embedding_y",
        color="predicted_subclass",
    )
    default_neighbor_fig = px.scatter(x=[0], y=[0])

    stub_utils = SimpleNamespace(
        get_nuc_id_from_seg_id=lambda x: x,
        find_nearest_neighbors=lambda df, cell_id, feature_set, n_neighbors: (
            [1],
            [10],
            [0.0],
        ),
        get_latest_seg_ids=lambda ids: ids,
        get_neuroglancer_link=lambda segment_ids: "https://example.org/ng",
    )
    stub_logger = SimpleNamespace(info=lambda *args, **kwargs: None)

    register_callbacks(
        app,
        umap_data=umap_data,
        default_scatter_fig=default_scatter_fig,
        default_neighbor_fig=default_neighbor_fig,
        utils_module=stub_utils,
        logger=stub_logger,
    )

    keys = list(app.callback_map.keys())

    assert len(keys) == 5
    assert any("default-scatter-plot.figure" in key for key in keys)
    assert any("default-neighbor-plot.figure" in key for key in keys)
    assert any("copy-trigger.children" in key for key in keys)
    assert any("neuroglancer-url-store.data" in key for key in keys)
    assert any("neuroglancer-open-trigger.children" in key for key in keys)
