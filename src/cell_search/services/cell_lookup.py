"""Cell ID lookup service functions."""

from __future__ import annotations

from cell_search.data_access import get_nucleus_table


def get_nuc_id_from_seg_id(cell_id, nuc_df=None):
    """Convert a segment ID to its corresponding nucleus ID."""
    if nuc_df is None:
        nuc_df = get_nucleus_table()

    seg_id = int(cell_id)
    nuc_id = nuc_df.query("pt_root_id == @seg_id").id.tolist()

    if len(nuc_id) == 0:
        return "Error: No nucleus found. Please use the most recent pt_root_id."
    if len(nuc_id) > 1:
        return "Error: Multiple nuclei found for this pt_root_id. Please refine your input."

    return nuc_id[0]


def get_latest_seg_ids(nuc_ids, nuc_df=None):
    """Convert nucleus IDs to their corresponding latest segment IDs."""
    if nuc_df is None:
        nuc_df = get_nucleus_table()

    updated_ids = []
    for nucleus_id in nuc_ids:
        seg_id = nuc_df.query("id == @nucleus_id").pt_root_id.tolist()[0]
        updated_ids.append(seg_id)
    return updated_ids
