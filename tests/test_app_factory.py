from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import flask
import pandas as pd

import cell_search.app as app_module


def _build_umap_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "umap_embedding_x": [0.0, 1.0],
            "umap_embedding_y": [0.0, 1.0],
            "predicted_class": ["a", "b"],
            "predicted_subclass": ["x", "y"],
            "nucleus_id": [1, 2],
        }
    )


def test_create_app_dash_on_flask_signature(monkeypatch) -> None:
    calls = []

    monkeypatch.setattr(app_module.pd, "read_parquet", lambda _path: _build_umap_df())

    def _register_callbacks(app, **kwargs):
        calls.append({"app": app, **kwargs})

    monkeypatch.setattr(app_module, "register_callbacks", _register_callbacks)

    server = flask.Flask("test-server")
    app = app_module.create_app(
        "cell-search",
        config={"data_path": "/tmp/test.parquet"},
        server=server,
        url_base_pathname="/dash/datastack/minnie/apps/cell_search/",
        meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    )

    assert app.server is server
    assert app.config.url_base_pathname == "/dash/datastack/minnie/apps/cell_search/"
    assert Path(app.config.assets_folder).name == "assets"
    assert calls
    assert calls[0]["app"] is app


def test_auth_token_hook_enabled_when_auth_disabled(monkeypatch) -> None:
    monkeypatch.setenv("AUTH_DISABLED", "true")
    monkeypatch.setenv("CAVE_TOKEN", "token-for-poc")
    monkeypatch.setattr(app_module.pd, "read_parquet", lambda _path: _build_umap_df())
    monkeypatch.setattr(
        app_module,
        "register_callbacks",
        lambda app, **kwargs: SimpleNamespace(app=app, **kwargs),
    )

    server = flask.Flask("test-server-auth-disabled")
    app_module.create_app("cell-search", server=server)

    with server.test_request_context("/"):
        server.preprocess_request()
        assert flask.g.auth_token == "token-for-poc"


def test_auth_token_hook_skipped_when_auth_enabled(monkeypatch) -> None:
    monkeypatch.setenv("AUTH_DISABLED", "false")
    monkeypatch.setenv("CAVE_TOKEN", "should-not-be-set")
    monkeypatch.setattr(app_module.pd, "read_parquet", lambda _path: _build_umap_df())
    monkeypatch.setattr(
        app_module,
        "register_callbacks",
        lambda app, **kwargs: SimpleNamespace(app=app, **kwargs),
    )

    server = flask.Flask("test-server-auth-enabled")
    app_module.create_app("cell-search", server=server)

    with server.test_request_context("/"):
        server.preprocess_request()
        assert not hasattr(flask.g, "auth_token")


def test_create_dash_app_standalone_builds_flask_server(monkeypatch) -> None:
    monkeypatch.setattr(app_module.pd, "read_parquet", lambda _path: _build_umap_df())
    monkeypatch.setattr(
        app_module,
        "register_callbacks",
        lambda app, **kwargs: SimpleNamespace(app=app, **kwargs),
    )

    app = app_module.create_dash_app(data_path="/tmp/test.parquet")

    assert isinstance(app.server, flask.Flask)
