`{bm-disable-all}`[ch7_code/src/sequence_phylogeny/NearestNeighbourInterchange.py](ch7_code/src/sequence_phylogeny/NearestNeighbourInterchange.py) (lines 49 to 110):`{bm-enable-all}`

```python
def list_nn_swap_options(
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


def nn_swap(
    tree: Graph[N, ND, E, ED],
    edge: E,
    side1: frozenset[E],
    side2: frozenset[E]
) -> tuple[
    frozenset[E],  # orig edges for side A
    frozenset[E]   # orig edges for side B
]:
    n1, n2 = tree.get_edge_ends(edge)
    n1_edges = set(tree.get_outputs(n1))
    n2_edges = set(tree.get_outputs(n2))
    n1_edges.remove(edge)
    n2_edges.remove(edge)
    assert n1_edges | n2_edges == side1 | side2
    edge_details = {}
    for e in side1 | side2:
        end1, end2, data = tree.get_edge(e)
        end = {end1, end2}.difference({n1, n2}).pop()
        edge_details[e] = (end, data)
        tree.delete_edge(e)
    for e in side1:
        end, data = edge_details[e]
        tree.insert_edge(e, n1, end, data)
    for e in side2:
        end, data = edge_details[e]
        tree.insert_edge(e, n2, end, data)
    return frozenset(n1_edges), frozenset(n2_edges)  # return original edges
```