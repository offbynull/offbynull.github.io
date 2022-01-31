`{bm-disable-all}`[ch8_code/src/clustering/Soft_HierarchialClustering_NeighbourJoining.py](ch8_code/src/clustering/Soft_HierarchialClustering_NeighbourJoining.py) (lines 92 to 115):`{bm-enable-all}`

```python
def soft_hierarchial_clustering_neighbour_joining(
        vectors: dict[str, tuple[float]],
        dims: int,
        distance_metric: DistanceMetric,
        gen_node_id: Callable[[], str],
        gen_edge_id: Callable[[], str]
) -> tuple[DistanceMatrix, Graph, ProbabilityMap]:
    # Generate a distance matrix from the vectors
    dists = {}
    for (k1, v1), (k2, v2) in product(vectors.items(), repeat=2):
        if k1 == k2:
            continue  # skip -- will default to 0
        dists[k1, k2] = distance_metric(v1, v2, dims)
    dist_mat = DistanceMatrix(dists)
    # Run neighbour joining phylogeny on the distance matrix
    tree = neighbour_joining_phylogeny(dist_mat, gen_node_id, gen_edge_id)
    # Compute leaf probabilities per internal node
    internal_nodes = [n for n in tree.get_nodes() if tree.get_degree(n) > 1]
    internal_node_probs = {}
    for n_i in internal_nodes:
        internal_node_probs[n_i] = leaf_probabilities(tree, n_i)
    # Return
    return dist_mat, tree, internal_node_probs
```