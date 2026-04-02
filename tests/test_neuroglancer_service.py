import pandas as pd
import pytest

from cell_search import utils
from cell_search.services import neuroglancer


def test_neuroglancer_service_centers_on_first_segment() -> None:
    class FakeViewerState:
        last_init_kwargs = None

        def __init__(self, **kwargs):
            FakeViewerState.last_init_kwargs = kwargs

        def add_image_layer(self, source, name):
            return self

        def add_segmentation_layer(self, source, name, segments):
            return self

        def to_url(self, client):
            return "https://example.org/ng-service"

    table = pd.DataFrame(
        {
            "id": [1],
            "pt_root_id": [999],
            "pt_position_x": [1000.0],
            "pt_position_y": [2000.0],
            "pt_position_z": [3000.0],
        }
    )

    url = neuroglancer.get_neuroglancer_link(
        segment_ids=[999],
        client_state_getter=lambda: (object(), "seg", "img"),
        nucleus_table_getter=lambda: table,
        viewer_state_class=FakeViewerState,
    )

    assert url == "https://example.org/ng-service"
    assert FakeViewerState.last_init_kwargs["position"] == [250000.0, 500000.0, 75000.0]


def test_neuroglancer_service_allows_empty_segments() -> None:
    class FakeViewerState:
        last_init_kwargs = None

        def __init__(self, **kwargs):
            FakeViewerState.last_init_kwargs = kwargs

        def add_image_layer(self, source, name):
            return self

        def add_segmentation_layer(self, source, name, segments):
            return self

        def to_url(self, client):
            return "https://example.org/ng-empty"

    url = neuroglancer.get_neuroglancer_link(
        segment_ids=[],
        client_state_getter=lambda: (object(), "seg", "img"),
        nucleus_table_getter=lambda: pd.DataFrame(),
        viewer_state_class=FakeViewerState,
    )

    assert url == "https://example.org/ng-empty"
    assert FakeViewerState.last_init_kwargs["position"] is None


def test_utils_get_neuroglancer_link_delegates_to_service(
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    captured = {}

    def _fake_get_neuroglancer_link(**kwargs):
        captured.update(kwargs)
        return "https://example.org/delegated"

    monkeypatch.setattr(
        neuroglancer, "get_neuroglancer_link", _fake_get_neuroglancer_link
    )

    result = utils.get_neuroglancer_link(segment_ids=[1, 2, 3])

    assert result == "https://example.org/delegated"
    assert captured["segment_ids"] == [1, 2, 3]
    assert captured["client_state_getter"] is utils._get_client_state
    assert captured["nucleus_table_getter"] is utils._get_nucleus_table
    assert captured["extract_xyz_fn"] is utils._extract_xyz_from_row
    assert captured["scale_position_fn"] is utils._scale_position_to_viewer
