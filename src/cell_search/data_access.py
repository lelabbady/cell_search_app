"""Data access helpers for client and lookup-table retrieval."""

from __future__ import annotations

from dash_connectivity_viewer.common.lookup_utilities import make_client

_client = None
_seg_source = None
_img_source = None
_nuc_df = None


def get_client_state():
    """Initialize and cache the CAVE client and source metadata."""
    global _client, _seg_source, _img_source

    if _client is None:
        _client = make_client(
            datastack="minnie65_public",
            server_address="https://global.daf-apis.com",
            materialize_version=None,
        )
        _seg_source = _client.info.segmentation_source()
        _img_source = _client.info.image_source()

    return _client, _seg_source, _img_source


def get_nucleus_table():
    """Load and cache the nucleus lookup table."""
    global _nuc_df

    if _nuc_df is None:
        client, _, _ = get_client_state()
        _nuc_df = client.materialize.query_view(
            "nucleus_detection_lookup_v1",
            split_positions=True,
            desired_resolution=(1000, 1000, 1000),
        )

    return _nuc_df


def reset_cache_for_tests() -> None:
    """Clear cached objects for deterministic tests."""
    global _client, _seg_source, _img_source, _nuc_df
    _client = None
    _seg_source = None
    _img_source = None
    _nuc_df = None
