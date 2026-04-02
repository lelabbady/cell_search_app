import pandas as pd
import pytest

from cell_search import utils
from cell_search.services import neighbor_search


def _build_df() -> pd.DataFrame:
    rows = []
    for i, nucleus_id in enumerate([101, 102, 103, 104]):
        row = {
            "nucleus_id": nucleus_id,
            "soma_id": 5000 + i,
        }
        for j, metric in enumerate(utils.soma_metrics):
            row[metric] = float(i * 10 + j)
        rows.append(row)
    return pd.DataFrame(rows)


def test_neighbor_search_service_returns_seed_first() -> None:
    df = _build_df()

    nuc_ids, soma_ids, distances = neighbor_search.find_nearest_neighbors(
        df=df,
        cell_id=101,
        feature_set="soma_metrics",
        n_neighbors=2,
        feature_dict=utils.feature_dict,
    )

    assert nuc_ids[0] == 101
    assert soma_ids[0] == 5000
    assert len(nuc_ids) == 3
    assert len(soma_ids) == 3
    assert len(distances) >= 3


def test_neighbor_search_service_is_deterministic_for_fixed_input() -> None:
    df = _build_df()

    first = neighbor_search.find_nearest_neighbors(
        df=df,
        cell_id=102,
        feature_set="soma_metrics",
        n_neighbors=2,
        feature_dict=utils.feature_dict,
    )
    second = neighbor_search.find_nearest_neighbors(
        df=df,
        cell_id=102,
        feature_set="soma_metrics",
        n_neighbors=2,
        feature_dict=utils.feature_dict,
    )

    assert first[0] == second[0]
    assert first[1] == second[1]
    assert (first[2] == second[2]).all()


def test_utils_find_nearest_neighbors_delegates_to_service(
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    captured = {}

    def _fake_find_nearest_neighbors(
        df, cell_id, feature_set, n_neighbors, feature_dict
    ):
        captured["cell_id"] = cell_id
        captured["feature_set"] = feature_set
        captured["n_neighbors"] = n_neighbors
        captured["feature_dict"] = feature_dict
        return [1], [2], [3.0]

    monkeypatch.setattr(
        neighbor_search, "find_nearest_neighbors", _fake_find_nearest_neighbors
    )

    result = utils.find_nearest_neighbors(
        df=pd.DataFrame(),
        cell_id=999,
        feature_set="soma_metrics",
        n_neighbors=5,
    )

    assert result == ([1], [2], [3.0])
    assert captured["cell_id"] == 999
    assert captured["feature_set"] == "soma_metrics"
    assert captured["n_neighbors"] == 5
    assert captured["feature_dict"] is utils.feature_dict
