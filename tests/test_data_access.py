"""Tests for data_access module-level configuration."""

from __future__ import annotations

import cell_search.data_access as da


def teardown_function():
    da.reset_cache_for_tests()


def test_configure_data_access_updates_datastack() -> None:
    da.configure_data_access(datastack="minnie65_phase3_v1")
    assert da._datastack == "minnie65_phase3_v1"


def test_configure_data_access_updates_server_address() -> None:
    da.configure_data_access(server_address="https://other.server.example.com")
    assert da._server_address == "https://other.server.example.com"


def test_configure_data_access_resets_cached_client() -> None:
    da._client = object()
    da._nuc_df = object()
    da.configure_data_access()
    assert da._client is None
    assert da._nuc_df is None


def test_reset_cache_for_tests_restores_defaults() -> None:
    da.configure_data_access(
        datastack="other_stack",
        server_address="https://other.server.example.com",
    )
    da.reset_cache_for_tests()
    assert da._datastack == "minnie65_public"
    assert da._server_address == "https://global.daf-apis.com"
    assert da._client is None
    assert da._nuc_df is None
