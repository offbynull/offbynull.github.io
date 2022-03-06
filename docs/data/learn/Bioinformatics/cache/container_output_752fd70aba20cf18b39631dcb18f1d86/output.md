`{bm-disable-all}`[ch8_code/src/clustering/SimilarityGraph_CAST.py](ch8_code/src/clustering/SimilarityGraph_CAST.py) (lines 178 to 198):`{bm-enable-all}`

```python
def cast(
        sim_graph: Graph,
        sim_mat: SimilarityMatrix,
        threshold: float
) -> list[set[str]]:
    # Copy similarity graph because it will get modified by this algorithm
    g = sim_graph.copy()
    # Pull out corrupted cliques and attempt to correct them
    clusters = []
    while len(g) > 0:
        _, start_n = max((g.get_degree(n), n) for n in g.get_nodes())  # highest degree node
        c = {start_n}
        consistent = False
        while not consistent:
            consistent = adjust_cluster(g, sim_mat, c, threshold)
        clusters.append(c)
        for n in c:
            if g.has_node(n):
                g.delete_node(n)
    return clusters
```