`{bm-disable-all}`[ch7_code/src/phylogeny/ExposeNeighbourParent_AdditiveExplainer.py](ch7_code/src/phylogeny/ExposeNeighbourParent_AdditiveExplainer.py) (lines 22 to 37):`{bm-enable-all}`

```python
def expose_neighbour_parent(
        dm: DistanceMatrix[N],
        l1: N,
        l2: N,
        gen_node_id: Callable[[], N]
) -> N:
    bald_distance_matrix(dm, l1)
    bald_distance_matrix(dm, l2)
    m_id = gen_node_id()
    m_dists = {x: (dm[l1, x] + dm[l2, x]) / 2 for x in dm.leaf_ids_it()}
    m_dists[m_id] = 0
    dm.insert(m_id, m_dists)
    dm.delete(l1)
    dm.delete(l2)
    return m_id
```