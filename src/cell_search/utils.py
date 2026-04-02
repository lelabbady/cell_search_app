import logging

from nglui import statebuilder

from cell_search.config import FEATURE_DICT, SOMA_METRICS
from cell_search.data_access import get_client_state, get_nucleus_table
from cell_search.services import cell_lookup, neighbor_search, neuroglancer

logger = logging.getLogger(__name__)

"""
Utility functions for cell search and analysis in connectomics data.
This module provides tools for finding similar cells based on morphological features,
managing cell IDs, and generating visualization links for neuroglancer.
Global Variables:
    soma_metrics: List of morphological feature names for soma analysis
    feature_dict: Dictionary mapping feature set names to feature lists
"""

NUCLEUS_TABLE_RESOLUTION = (1000.0, 1000.0, 1000.0)
VIEWER_RESOLUTION = (4.0, 4.0, 40.0)

soma_metrics = SOMA_METRICS
feature_dict = FEATURE_DICT


def _get_client_state():
    """Compatibility wrapper for data_access.get_client_state."""
    return get_client_state()


def _get_nucleus_table():
    """Compatibility wrapper for data_access.get_nucleus_table."""
    return get_nucleus_table()


def _extract_xyz_from_row(row):
    """Return pt-position xyz coordinates from a nucleus table row when available."""
    required_cols = ("pt_position_x", "pt_position_y", "pt_position_z")
    if all(col in row for col in required_cols):
        return [
            float(row[required_cols[0]]),
            float(row[required_cols[1]]),
            float(row[required_cols[2]]),
        ]
    return None


def _scale_position_to_viewer(position_xyz):
    """Convert table-space positions to viewer-space voxel coordinates."""
    if position_xyz is None:
        return None

    scaled = [
        position_xyz[0] * (NUCLEUS_TABLE_RESOLUTION[0] / VIEWER_RESOLUTION[0]),
        position_xyz[1] * (NUCLEUS_TABLE_RESOLUTION[1] / VIEWER_RESOLUTION[1]),
        position_xyz[2] * (NUCLEUS_TABLE_RESOLUTION[2] / VIEWER_RESOLUTION[2]),
    ]
    return scaled


def get_nuc_id_from_seg_id(cell_id):
    """
    Convert a segment ID to its corresponding nucleus ID.
    Args:
        cell_id: Segment ID (pt_root_id) to convert
    Returns:
        int: Nucleus ID if found
        str: Error message if no nucleus found or multiple nuclei found
    """
    nuc_df = _get_nucleus_table()
    return cell_lookup.get_nuc_id_from_seg_id(cell_id=cell_id, nuc_df=nuc_df)


def get_latest_seg_ids(nuc_ids):
    """
    Convert nucleus IDs to their corresponding latest segment IDs.
    Args:
        nuc_ids (list): List of nucleus IDs to convert
    Returns:
        list: List of corresponding pt_root_ids (segment IDs)
    """
    nuc_df = _get_nucleus_table()
    return cell_lookup.get_latest_seg_ids(nuc_ids=nuc_ids, nuc_df=nuc_df)


def find_nearest_neighbors(df, cell_id, feature_set, n_neighbors):
    """
    Find the nearest neighboring cells based on morphological features using KDTree.
    Uses standardized features and Euclidean distance in high-dimensional space
    to identify cells with similar morphological properties.
    Args:
        df (pandas.DataFrame): DataFrame containing cell data with features
        cell_id (int): Nucleus ID of the target cell
        feature_set (str): Key for feature_dict specifying which features to use
        n_neighbors (int): Number of nearest neighbors to return
    Returns:
        tuple: A tuple containing:
            - similar_neuron_nuc_ids (list): Nucleus IDs of similar cells
            - similar_neurons (list): Soma IDs of similar cells
            - broad_distances (array): Distances to a broader set of neighbors
    """

    return neighbor_search.find_nearest_neighbors(
        df=df,
        cell_id=cell_id,
        feature_set=feature_set,
        n_neighbors=n_neighbors,
        feature_dict=feature_dict,
    )


def get_neuroglancer_link(segment_ids=None):
    """
    Generate a neuroglancer visualization URL for specified segments.
    Creates a viewer state with image and segmentation layers, highlighting
    the provided segment IDs for visualization.
    Args:
        segment_ids (list, optional): List of segment IDs to highlight.
                                    Defaults to empty list.
    Returns:
        str: URL for neuroglancer viewer with the specified segments
    """

    return neuroglancer.get_neuroglancer_link(
        segment_ids=segment_ids,
        client_state_getter=_get_client_state,
        nucleus_table_getter=_get_nucleus_table,
        viewer_state_class=statebuilder.ViewerState,
        extract_xyz_fn=_extract_xyz_from_row,
        scale_position_fn=_scale_position_to_viewer,
    )


if __name__ == "__main__":
    logger.info("The utils script is being run directly.")
