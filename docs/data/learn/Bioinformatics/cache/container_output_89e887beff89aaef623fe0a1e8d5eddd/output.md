`{bm-disable-all}`[ch8_code/src/clustering/Soft_HierarchialClustering_NeighbourJoining_v2.py](ch8_code/src/clustering/Soft_HierarchialClustering_NeighbourJoining_v2.py) (lines 78 to 98):`{bm-enable-all}`

```python
def estimate_ownership(
        tree: Graph[str, None, str, float],
        dist_capture: float
) -> tuple[dict[str, str], dict[str, str]]:
    # Assign leaf nodes to each internal node based on distance. That distance
    # is compared against the distorted average to determine assignment.
    #
    # The same leaf node may be assigned to multiple different internal nodes.
    internal_to_leaves = {}
    leaves_to_internal = {}
    internal_nodes = {n for n in tree.get_nodes() if tree.get_degree(n) > 1}
    for n_i in internal_nodes:
        leaf_dists = get_leaf_distances(tree, n_i)
        for n_l, dist in leaf_dists.items():
            if dist > dist_capture:
                continue
            internal_to_leaves.setdefault(n_i, set()).add(n_l)
            leaves_to_internal.setdefault(n_l, set()).add(n_i)
    # Return assignments
    return internal_to_leaves, leaves_to_internal
```