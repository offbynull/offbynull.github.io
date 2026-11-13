`{bm-disable-all}`[ch7_code/src/phylogeny/AdditivePhylogeny.py](ch7_code/src/phylogeny/AdditivePhylogeny.py) (lines 34 to 49):`{bm-enable-all}`

```python
def to_obvious_graph(
        dm: DistanceMatrix[N],
        gen_edge_id: Callable[[], E]
) -> Graph[N, ND, E, float]:
    if dm.n != 2:
        raise ValueError('Distance matrix must only contain 2 leaf nodes')
    l1, l2 = dm.leaf_ids()
    g = Graph()
    g.insert_node(l1)
    g.insert_node(l2)
    g.insert_edge(
        gen_edge_id(),
        l1,
        l2,
        dm[l1, l2]
    )
    return g
```