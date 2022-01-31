`{bm-disable-all}`[ch8_code/src/clustering/HierarchialClustering_UPGMA.py](ch8_code/src/clustering/HierarchialClustering_UPGMA.py) (lines 49 to 65):`{bm-enable-all}`

```python
def hierarchial_clustering_upgma(
        vectors: dict[str, tuple[float]],
        dims: int,
        distance_metric: DistanceMetric
) -> tuple[DistanceMatrix, Graph]:
    # Generate a distance matrix from the vectors
    dists = {}
    for (k1, v1), (k2, v2) in product(vectors.items(), repeat=2):
        if k1 == k2:
            continue  # skip -- will default to 0
        dists[k1, k2] = distance_metric(v1, v2, dims)
    dist_mat = DistanceMatrix(dists)
    # Run UPGMA on the distance matrix
    tree, _ = upgma(dist_mat.copy())
    # Return
    return dist_mat, tree
```