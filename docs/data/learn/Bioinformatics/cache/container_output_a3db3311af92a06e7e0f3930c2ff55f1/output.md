`{bm-disable-all}`[ch8_code/src/clustering/Soft_HierarchialClustering_NeighbourJoining_v2.py](ch8_code/src/clustering/Soft_HierarchialClustering_NeighbourJoining_v2.py) (lines 144 to 162):`{bm-enable-all}`

```python
def clustering_neighbour_joining(
        tree: Graph[str, None, str, float],
        dist_capture: float
) -> Clusters:
    # Find clusters by estimating which internal node owns which leaf node (there may be multiple
    # estimated owners), then merge overlapping estimates.
    internal_to_leaves, leaves_to_internal = estimate_ownership(tree, dist_capture)
    clusters = []
    while len(leaves_to_internal) > 0:
        n_leaf = next(iter(leaves_to_internal))
        n_leaves, n_internals = merge_overlaps(n_leaf, internal_to_leaves, leaves_to_internal)
        for n in n_internals:
            del internal_to_leaves[n]
        for n in n_leaves:
            del leaves_to_internal[n]
        if len(n_leaves) > 1:  # cluster of 1 is not a cluster
            clusters.append(n_leaves | n_internals)
    return clusters
```