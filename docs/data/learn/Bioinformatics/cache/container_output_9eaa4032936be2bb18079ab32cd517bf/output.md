`{bm-disable-all}`[ch7_code/src/phylogeny/AdditivePhylogeny.py](ch7_code/src/phylogeny/AdditivePhylogeny.py) (lines 55 to 68):`{bm-enable-all}`

```python
def additive_phylogeny(
        dm: DistanceMatrix[N],
        gen_node_id: Callable[[], N],
        gen_edge_id: Callable[[], E]
) -> Graph:
    if dm.n == 2:
        return to_obvious_graph(dm, gen_edge_id)
    n = next(dm.leaf_ids_it())
    dm_untrimmed = dm.copy()
    trim_distance_matrix(dm, n)
    g = additive_phylogeny(dm, gen_node_id, gen_edge_id)
    untrim_tree(dm_untrimmed, g, gen_node_id, gen_edge_id)
    return g
```