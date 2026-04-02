"""Neuroglancer service functions."""

from __future__ import annotations

from nglui import statebuilder

from cell_search.data_access import get_client_state, get_nucleus_table

NUCLEUS_TABLE_RESOLUTION = (1000.0, 1000.0, 1000.0)
VIEWER_RESOLUTION = (4.0, 4.0, 40.0)


def extract_xyz_from_row(row):
    """Return xyz coordinates from a nucleus-table row when present."""
    required_cols = ("pt_position_x", "pt_position_y", "pt_position_z")
    if all(col in row for col in required_cols):
        return [
            float(row[required_cols[0]]),
            float(row[required_cols[1]]),
            float(row[required_cols[2]]),
        ]
    return None


def scale_position_to_viewer(position_xyz):
    """Convert nucleus-table coordinates into viewer voxel coordinates."""
    if position_xyz is None:
        return None

    return [
        position_xyz[0] * (NUCLEUS_TABLE_RESOLUTION[0] / VIEWER_RESOLUTION[0]),
        position_xyz[1] * (NUCLEUS_TABLE_RESOLUTION[1] / VIEWER_RESOLUTION[1]),
        position_xyz[2] * (NUCLEUS_TABLE_RESOLUTION[2] / VIEWER_RESOLUTION[2]),
    ]


def get_neuroglancer_link(
    segment_ids=None,
    *,
    client_state_getter=get_client_state,
    nucleus_table_getter=get_nucleus_table,
    viewer_state_class=statebuilder.ViewerState,
    extract_xyz_fn=extract_xyz_from_row,
    scale_position_fn=scale_position_to_viewer,
):
    """Generate a neuroglancer URL for the selected segments."""
    if segment_ids is None:
        segment_ids = []

    client, seg_source, img_source = client_state_getter()
    center_position = None

    if segment_ids:
        first_seg_id = int(segment_ids[0])
        nuc_df = nucleus_table_getter()
        row_match = nuc_df.query("pt_root_id == @first_seg_id")
        if not row_match.empty:
            raw_position = extract_xyz_fn(row_match.iloc[0])
            center_position = scale_position_fn(raw_position)

    viewer_state = (
        viewer_state_class(
            dimensions=[4, 4, 40],
            position=center_position,
            infer_coordinates=False,
        )
        .add_image_layer(source=img_source, name="emdata")
        .add_segmentation_layer(
            source=seg_source,
            name="seg",
            segments=segment_ids,
        )
    )
    return viewer_state.to_url(client=client)
