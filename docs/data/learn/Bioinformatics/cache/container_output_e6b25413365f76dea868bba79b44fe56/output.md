`{bm-disable-all}`[ch7_code/src/phylogeny/MergeNeighbours_Optimized.py](ch7_code/src/phylogeny/MergeNeighbours_Optimized.py) (lines 22 to 34):`{bm-enable-all}`

```python
def bald_and_merge_neighbours(
        dm: DistanceMatrix,
        l1: N,
        l2: N,
        gen_node_id: Callable[[], str]
) -> None:
    m_id = gen_node_id()
    m_dists = {x: (dm[l1, x] + dm[l2, x] - dm[l1, l2]) / 2 for x in dm.leaf_ids_it()}
    m_dists[m_id] = 0
    dm.insert(m_id, m_dists)
    dm.delete(l1)
    dm.delete(l2)
```