`{bm-disable-all}`[ch7_code/src/phylogeny/ExposeNeighbourParent.py](ch7_code/src/phylogeny/ExposeNeighbourParent.py) (lines 23 to 50):`{bm-enable-all}`

```python
def expose_neighbour_parent(
        dm: DistanceMatrix,
        l1: N,
        l2: N,
        gen_node_id: Callable[[], str]
) -> N:
    # bald
    l1_len_views = {}
    l2_len_views = {}
    for x in dm.leaf_ids_it():
        if x == l1 or x == l2:
            continue
        l1_len_views[x] = view_of_limb_length_using_neighbour(dm, l1, l2, x)
        l2_len_views[x] = view_of_limb_length_using_neighbour(dm, l2, l1, x)
    for x in dm.leaf_ids_it():
        if x == l1 or x == l2:
            continue
        dm[l1, x] = dm[l1, x] - l1_len_views[x]
        dm[l2, x] = dm[l2, x] - l2_len_views[x]
    # merge
    m_id = gen_node_id()
    m_dists = {x: (dm[l1, x] + dm[l2, x]) / 2 for x in dm.leaf_ids_it()}
    m_dists[m_id] = 0
    dm.insert(m_id, m_dists)
    dm.delete(l1)
    dm.delete(l2)
    return m_id
```