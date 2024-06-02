import numpy as np

def compute_partial_parents(parents):
    """Computes the partial parents of a parents vector"""
    parented_idxs = np.where(parents >= 0)[0]
    partial_parents = parents[parented_idxs]
    for i, node in enumerate(parented_idxs + 1):
        partial_parents[partial_parents == node] = i + 1
    return partial_parents

def parents_to_adj(parents):
    """Converts an incomplete parents vector to an equivalent adjacency matrix"""
    K = len(parents) + 1
    adj = np.eye(K)
    adj[parents[parents >= 0], np.where(parents >= 0)[0] + 1] = 1
    return adj

   