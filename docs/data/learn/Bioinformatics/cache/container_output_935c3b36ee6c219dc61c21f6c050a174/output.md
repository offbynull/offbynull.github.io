`{bm-disable-all}`[ch7_code/src/sequence_phylogeny/NearestNeighbourInterchange.py](ch7_code/src/sequence_phylogeny/NearestNeighbourInterchange.py) (lines 49 to 79):`{bm-enable-all}`

```python
def nearest_neighbour_interchange_options(
        tree: Graph[N, ND, E, ED],
        edge: E
) -> set[
    tuple[
        frozenset[E],  # side1 edges
        frozenset[E]   # side2 edges
    ]
]:
    n1, n2 = tree.get_edge_ends(edge)
    n1_edges = set(tree.get_outputs(n1))
    n2_edges = set(tree.get_outputs(n2))
    n1_edges.remove(edge)
    n2_edges.remove(edge)
    n1_edges = frozenset(n1_edges)
    n2_edges = frozenset(n2_edges)
    n1_edge_cnt = len(n1_edges)
    n2_edge_cnt = len(n2_edges)
    both_edges = n1_edges | n2_edges
    ret = set()
    for n1_edges_perturbed in combinations(both_edges, n1_edge_cnt):
        n1_edges_perturbed = frozenset(n1_edges_perturbed)
        n2_edges_perturbed = frozenset(both_edges.difference(n1_edges_perturbed))
        if (n1_edges_perturbed, n2_edges_perturbed) in ret:
            continue
        if (n2_edges_perturbed, n1_edges_perturbed) in ret:
            continue
        if {n1_edges_perturbed, n2_edges_perturbed} == {n1_edges, n2_edges}:
            continue
        ret.add((n1_edges_perturbed, n2_edges_perturbed))
    return ret
```