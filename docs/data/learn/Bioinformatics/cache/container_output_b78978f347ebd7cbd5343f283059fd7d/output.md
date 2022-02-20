```python
def adjust_cluster(
        sim_graph: Graph,
        sim_mat: SimilarityMatrix,
        cluster: set[str],
        threshold: float
) -> bool:
    # Add closest NOT in cluster
    outside_cluster = set(n for n in sim_graph.get_nodes() if n not in cluster)
    closest = max(
        ((similarity_to_cluster(n, cluster, sim_mat), n) for n in outside_cluster),
        default=None
    )
    add_closest = closest is not None and closest[0] > threshold
    if add_closest:
        cluster.add(closest[1])
    # Remove farthest in cluster
    farthest = min(
        ((similarity_to_cluster(n, cluster, sim_mat), n) for n in cluster),
        default=None
    )
    remove_farthest = farthest is not None and farthest[0] <= threshold
    if remove_farthest:
        cluster.remove(farthest[1])
    # Return true if cluster didn't change (consistent cluster)
    return not add_closest and not remove_farthest
```