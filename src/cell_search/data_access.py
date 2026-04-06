"""Data access helpers for client and lookup-table retrieval."""

from __future__ import annotations

from dash_connectivity_viewer.common.lookup_utilities import make_client

_datastack: str = "minnie65_public"
_server_address: str = "https://global.daf-apis.com"
_client = None
_seg_source = None
_img_source = None
_nuc_df = None


def configure_data_access(
    datastack: str = "minnie65_public",
    server_address: str = "https://global.daf-apis.com",
) -> None:
    """Configure the CAVE client parameters and reset the cached state.

    Call this once during app initialization (e.g., from ``create_app``)
    before any request-time lookups occur.

    Args:
        datastack: CAVE datastack name (e.g. ``"minnie65_public"``).
        server_address: Base URL of the CAVE server.
    """
    global _datastack, _server_address, _client, _seg_source, _img_source, _nuc_df
    _datastack = datastack
    _server_address = server_address
    _client = None
    _seg_source = None
    _img_source = None
    _nuc_df = None


def get_client_state():
    """Initialize and cache the CAVE client and source metadata."""
    global _client, _seg_source, _img_source

    if _client is None:
        _client = make_client(
            datastack=_datastack,
            server_address=_server_address,
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
    """Clear cached objects and configuration for deterministic tests."""
    global _datastack, _server_address, _client, _seg_source, _img_source, _nuc_df
    _datastack = "minnie65_public"
    _server_address = "https://global.daf-apis.com"
    _client = None
    _seg_source = None
    _img_source = None
    _nuc_df = None
