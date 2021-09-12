`{bm-disable-all}`[ch7_code/src/phylogeny/TreeToSimpleTree.py](ch7_code/src/phylogeny/TreeToSimpleTree.py) (lines 88 to 105):`{bm-enable-all}`

```python
def merge_nodes_of_degree2(g: Graph[N, ND, E, float]) -> None:
    # Can be made more efficient by not having to re-collect bad nodes each
    # iteration. Kept it like this so it's simple to understand what's going on.
    while True:
        bad_nodes = {n for n in g.get_nodes() if g.get_degree(n) == 2}
        if len(bad_nodes) == 0:
            return
        bad_n = bad_nodes.pop()
        bad_e1, bad_e2 = tuple(g.get_outputs(bad_n))
        e_id = bad_e1 + bad_e2
        e_n1 = [n for n in g.get_edge_ends(bad_e1) if n != bad_n][0]
        e_n2 = [n for n in g.get_edge_ends(bad_e2) if n != bad_n][0]
        e_weight = g.get_edge_data(bad_e1) + g.get_edge_data(bad_e2)
        g.insert_edge(e_id, e_n1, e_n2, e_weight)
        g.delete_edge(bad_e1)
        g.delete_edge(bad_e2)
        g.delete_node(bad_n)
```