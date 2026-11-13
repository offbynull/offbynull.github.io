`{bm-disable-all}`[ch7_code/src/phylogeny/NeighbourJoiningPhylogeny.py](ch7_code/src/phylogeny/NeighbourJoiningPhylogeny.py) (lines 69 to 86):`{bm-enable-all}`

```python
def neighbour_joining_phylogeny(
        dm: DistanceMatrix,
        gen_node_id: Callable[[], N],
        gen_edge_id: Callable[[], E]
) -> Graph:
    if dm.n == 2:
        return to_obvious_graph(dm, gen_edge_id)
    l1, l2 = find_neighbours(dm)
    l1_len, l2_len = find_neighbouring_limb_lengths(dm, l1, l2)
    dm_trimmed = dm.copy()
    p = expose_neighbour_parent(dm_trimmed, l1, l2, gen_node_id)  # p added to dm_trimmed while l1, l2 removed
    g = neighbour_joining_phylogeny(dm_trimmed, gen_node_id, gen_edge_id)
    g.insert_node(l1)
    g.insert_node(l2)
    g.insert_edge(gen_edge_id(), p, l1, l1_len)
    g.insert_edge(gen_edge_id(), p, l2, l2_len)
    return g
```