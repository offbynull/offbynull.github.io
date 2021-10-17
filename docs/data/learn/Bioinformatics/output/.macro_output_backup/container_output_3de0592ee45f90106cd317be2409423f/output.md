`{bm-disable-all}`[ch7_code/src/phylogeny/AdditivePhylogeny.py](ch7_code/src/phylogeny/AdditivePhylogeny.py) (lines 31 to 46):`{bm-enable-all}`

```python
def to_obvious_graph(
        dm: DistanceMatrix,
        gen_edge_id: Callable[[], str]
) -> Graph:
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