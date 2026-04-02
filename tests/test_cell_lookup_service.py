import pandas as pd

from cell_search.services import cell_lookup


def test_service_get_nuc_id_from_seg_id_returns_expected_id() -> None:
    nuc_df = pd.DataFrame({"id": [1001, 1002], "pt_root_id": [9001, 9002]})

    result = cell_lookup.get_nuc_id_from_seg_id(9002, nuc_df=nuc_df)

    assert result == 1002


def test_service_get_nuc_id_from_seg_id_returns_missing_error() -> None:
    nuc_df = pd.DataFrame({"id": [1001], "pt_root_id": [9001]})

    result = cell_lookup.get_nuc_id_from_seg_id(9999, nuc_df=nuc_df)

    assert result == "Error: No nucleus found. Please use the most recent pt_root_id."


def test_service_get_nuc_id_from_seg_id_returns_multiple_match_error() -> None:
    nuc_df = pd.DataFrame({"id": [1001, 1002], "pt_root_id": [9001, 9001]})

    result = cell_lookup.get_nuc_id_from_seg_id(9001, nuc_df=nuc_df)

    assert (
        result
        == "Error: Multiple nuclei found for this pt_root_id. Please refine your input."
    )


def test_service_get_latest_seg_ids_preserves_input_order() -> None:
    nuc_df = pd.DataFrame({"id": [1, 2, 3], "pt_root_id": [4001, 4002, 4003]})

    result = cell_lookup.get_latest_seg_ids([3, 1], nuc_df=nuc_df)

    assert result == [4003, 4001]
