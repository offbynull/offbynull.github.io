`{bm-disable-all}`[ch8_code/src/clustering/SimilarityGraph_CAST.py](ch8_code/src/clustering/SimilarityGraph_CAST.py) (lines 47 to 74):`{bm-enable-all}`

```python
def similarity_graph(
        vectors: dict[str, tuple[float, ...]],
        dims: int,
        similarity_metric: SimilarityMetric,
        threshold: float,
) -> tuple[Graph, SimilarityMatrix]:
    # Generate similarity matrix from the vectors
    dists = {}
    for (k1, v1), (k2, v2) in product(vectors.items(), repeat=2):
        dists[k1, k2] = similarity_metric(v1, v2, dims)
    sim_mat = SimilarityMatrix(dists)
    # Generate similarity graph
    nodes = sim_mat.leaf_ids()
    sim_graph = Graph()
    for n in nodes:
        sim_graph.insert_node(n)
    for n1, n2 in product(nodes, repeat=2):
        if n1 == n2:
            continue
        e = f'E{sorted([n1, n2])}'
        if sim_graph.has_edge(e):
            continue
        if sim_mat[n1, n2] < threshold:
            continue
        sim_graph.insert_edge(e, n1, n2)
    # Return
    return sim_graph, sim_mat
```