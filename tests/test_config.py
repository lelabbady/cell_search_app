from pathlib import Path

import pytest

from cell_search import config


def test_resolve_data_path_uses_default_when_no_overrides(
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    monkeypatch.delenv(config.DATA_PATH_ENV_VAR, raising=False)

    resolved = config.resolve_data_path()

    assert resolved == config.DEFAULT_DATA_PATH


def test_resolve_data_path_uses_environment_override(
    monkeypatch: "pytest.MonkeyPatch", tmp_path: Path
) -> None:
    env_path = tmp_path / "custom.parquet"
    monkeypatch.setenv(config.DATA_PATH_ENV_VAR, str(env_path))

    resolved = config.resolve_data_path()

    assert resolved == env_path.resolve()


def test_resolve_data_path_prefers_explicit_argument(
    monkeypatch: "pytest.MonkeyPatch", tmp_path: Path
) -> None:
    monkeypatch.setenv(config.DATA_PATH_ENV_VAR, str(tmp_path / "env.parquet"))
    explicit = tmp_path / "explicit.parquet"

    resolved = config.resolve_data_path(str(explicit))

    assert resolved == explicit.resolve()


def test_feature_dict_contains_default_feature_set() -> None:
    assert config.DEFAULT_FEATURE_SET in config.FEATURE_DICT
    assert config.FEATURE_DICT[config.DEFAULT_FEATURE_SET] == config.SOMA_METRICS
