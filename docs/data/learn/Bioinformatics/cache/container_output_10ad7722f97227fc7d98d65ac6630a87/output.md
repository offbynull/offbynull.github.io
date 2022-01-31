`{bm-disable-all}`[ch8_code/src/clustering/Soft_HierarchialClustering_NeighbourJoining.py](ch8_code/src/clustering/Soft_HierarchialClustering_NeighbourJoining.py) (lines 68 to 84):`{bm-enable-all}`

```python
def leaf_probabilities(
        tree: Graph[str, None, str, float],
        n: str,
) -> dict[str, float]:
    # Get dists between n and each to leaf node
    dists = {}
    get_leaf_distances(tree, n, None, 0.0, dists)
    # Calculate inverse distance weighting
    #   See: https://stackoverflow.com/a/23524954
    #   The link talks about a "stiffness" parameter similar to the stiffness parameter in the
    #   partition function used for soft k-means clustering. In this case, you can make the
    #   probabilities more decisive by taking the the distance to the power of X, where larger
    #   X values give more decisive probabilities.
    inverse_dists = {leaf: 1.0/d for leaf, d in dists.items()}
    inverse_dists_total = sum(inverse_dists.values())
    return {leaf: inv_dist / inverse_dists_total for leaf, inv_dist in inverse_dists.items()}
```