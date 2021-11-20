`{bm-disable-all}`[ch7_code/src/sequence_phylogeny/NearestNeighbourInterchange.py](ch7_code/src/sequence_phylogeny/NearestNeighbourInterchange.py) (lines 84 to 112):`{bm-enable-all}`

```python
def interchange_neighbours(
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