```python
def similarity_to_cluster(
        n: str,
        cluster: set[str],
        sim_mat: SimilarityMatrix
) -> float:
    return mean(sim_mat[n, n_c] for n_c in cluster)
```