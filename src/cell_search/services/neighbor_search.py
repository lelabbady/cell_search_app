"""Neighbor search service functions."""

from __future__ import annotations

import logging

from sklearn import preprocessing
from sklearn.neighbors import KDTree

from cell_search.config import FEATURE_DICT

logger = logging.getLogger(__name__)


def find_nearest_neighbors(
    df,
    cell_id,
    feature_set,
    n_neighbors,
    feature_dict=None,
):
    """Find nearest neighbors using standardized feature-space KDTree distance."""
    active_feature_dict = FEATURE_DICT if feature_dict is None else feature_dict

    df = df.reset_index(drop=True)
    feature_values = active_feature_dict[feature_set]
    cell_features = df[feature_values].to_numpy()

    scaler = preprocessing.StandardScaler().fit(cell_features)
    cell_features_normalized = scaler.transform(cell_features)
    n_features = len(feature_values)
    cell_id = int(cell_id)

    kdt = KDTree(cell_features_normalized, leaf_size=30, metric="euclidean")

    idx = df.query("nucleus_id == @cell_id").index[0]
    X = cell_features_normalized[idx, :].reshape(1, n_features)

    n_cells = cell_features_normalized.shape[0]
    all_distances, all_idxs = kdt.query(X, k=n_cells, return_distance=True)
    broad_distances = all_distances[0][: (n_neighbors * 10) + 1]
    similar_idxs = all_idxs[0][: n_neighbors + 1]
    similar_neurons = df.soma_id.iloc[similar_idxs].tolist()
    similar_neuron_nuc_ids = df.nucleus_id.iloc[similar_idxs].tolist()
    logger.info("similar neurons: %s", similar_neurons)

    return similar_neuron_nuc_ids, similar_neurons, broad_distances
