import pandas as pd
import pytest

from cell_search import utils


def _build_feature_df() -> pd.DataFrame:
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


def test_extract_xyz_from_row_returns_values_when_present() -> None:
    row = {
        "pt_position_x": 1,
        "pt_position_y": 2,
        "pt_position_z": 3,
    }

    result = utils._extract_xyz_from_row(row)

    assert result == [1.0, 2.0, 3.0]


def test_extract_xyz_from_row_returns_none_when_missing() -> None:
    row = {"pt_position_x": 1, "pt_position_y": 2}

    result = utils._extract_xyz_from_row(row)

    assert result is None


def test_scale_position_to_viewer_scales_correctly() -> None:
    scaled = utils._scale_position_to_viewer([1000.0, 2000.0, 3000.0])

    assert scaled == [250000.0, 500000.0, 75000.0]


def test_get_nuc_id_from_seg_id_returns_expected_nucleus(
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    table = pd.DataFrame(
        {
            "id": [11, 12],
            "pt_root_id": [9001, 9002],
        }
    )
    monkeypatch.setattr(utils, "_get_nucleus_table", lambda: table)

    result = utils.get_nuc_id_from_seg_id("9001")

    assert result == 11


def test_get_nuc_id_from_seg_id_returns_error_when_missing(
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    table = pd.DataFrame(
        {
            "id": [11],
            "pt_root_id": [9001],
        }
    )
    monkeypatch.setattr(utils, "_get_nucleus_table", lambda: table)

    result = utils.get_nuc_id_from_seg_id(9999)

    assert result == "Error: No nucleus found. Please use the most recent pt_root_id."


def test_get_latest_seg_ids_uses_nucleus_lookup(
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    table = pd.DataFrame(
        {
            "id": [21, 22, 23],
            "pt_root_id": [7001, 7002, 7003],
        }
    )
    monkeypatch.setattr(utils, "_get_nucleus_table", lambda: table)

    result = utils.get_latest_seg_ids([23, 21])

    assert result == [7003, 7001]


def test_find_nearest_neighbors_returns_self_first_and_requested_count() -> None:
    df = _build_feature_df()

    nuc_ids, soma_ids, distances = utils.find_nearest_neighbors(
        df=df,
        cell_id=101,
        feature_set="soma_metrics",
        n_neighbors=2,
    )

    assert len(nuc_ids) == 3
    assert len(soma_ids) == 3
    assert nuc_ids[0] == 101
    assert soma_ids[0] == 5000
    assert len(distances) >= 3


def test_get_neuroglancer_link_centers_from_first_segment(
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    class FakeViewerState:
        last_init_kwargs = None

        def __init__(self, **kwargs):
            FakeViewerState.last_init_kwargs = kwargs

        def add_image_layer(self, source, name):
            return self

        def add_segmentation_layer(self, source, name, segments):
            return self

        def to_url(self, client):
            return "https://example.org/ng"

    class FakeStateBuilder:
        ViewerState = FakeViewerState

    table = pd.DataFrame(
        {
            "id": [1],
            "pt_root_id": [999],
            "pt_position_x": [1000.0],
            "pt_position_y": [2000.0],
            "pt_position_z": [3000.0],
        }
    )

    monkeypatch.setattr(utils, "_get_nucleus_table", lambda: table)
    monkeypatch.setattr(utils, "_get_client_state", lambda: (object(), "seg", "img"))
    monkeypatch.setattr(utils, "statebuilder", FakeStateBuilder)

    url = utils.get_neuroglancer_link(segment_ids=[999, 1000])

    assert url == "https://example.org/ng"
    assert FakeViewerState.last_init_kwargs["position"] == [250000.0, 500000.0, 75000.0]
