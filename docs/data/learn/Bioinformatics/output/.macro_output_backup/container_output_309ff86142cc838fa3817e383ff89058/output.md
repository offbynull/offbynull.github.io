`{bm-disable-all}`[ch7_code/src/phylogeny/TreeToAdditiveDistanceMatrix.py](ch7_code/src/phylogeny/TreeToAdditiveDistanceMatrix.py) (lines 39 to 69):`{bm-enable-all}`

```python
def find_path(g: Graph, n1: N, n2: N) -> list[E]:
    if not g.has_node(n1) or not g.has_node(n2):
        ValueError('Node missing')
    if n1 == n2:
        return []
    queued_edges = list()
    for e in g.get_outputs(n1):
        queued_edges.append((n1, [e]))
    while len(queued_edges) > 0:
        ignore_n, e_list = queued_edges.pop()
        e_last = e_list[-1]
        active_n = [n for n in g.get_edge_ends(e_last) if n != ignore_n][0]
        if active_n == n2:
            return e_list
        children = set(g.get_outputs(active_n))
        children.remove(e_last)
        for child_e in children:
            child_ignore_n = active_n
            new_e_list = e_list[:] + [child_e]
            queued_edges.append((child_ignore_n, new_e_list))
    raise ValueError(f'No path from {n1} to {n2}')


def to_additive_distance_matrix(g: Graph[N, ND, E, float]) -> DistanceMatrix[N]:
    leaves = {n for n in g.get_nodes() if g.get_degree(n) == 1}
    dists = {}
    for l1, l2 in product(leaves, repeat=2):
        d = sum(g.get_edge_data(e) for e in find_path(g, l1, l2))
        dists[l1, l2] = d
    return DistanceMatrix(dists)
```