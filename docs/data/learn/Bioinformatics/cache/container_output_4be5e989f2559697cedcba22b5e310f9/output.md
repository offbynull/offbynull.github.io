`{bm-disable-all}`[ch7_code/src/sequence_phylogeny/ParsimonyScore.py](ch7_code/src/sequence_phylogeny/ParsimonyScore.py) (lines 47 to 71):`{bm-enable-all}`

```python
def populate_edge_similarity(
        g: Graph[N, ND, E, ED],
        get_sequence: Callable[[ND], str],
        set_weight: Callable[[ED, float], None]
) -> None:
    for e in g.get_edges():
        n1, n2, e_data = g.get_edge(e)
        n1_data = g.get_node_data(n1)
        n2_data = g.get_node_data(n2)
        n1_seq = get_sequence(n1_data)
        n2_seq = get_sequence(n2_data)
        weight = hamming_distance(n1_seq, n2_seq)
        set_weight(e_data, weight)


def parsimony_score(
        g: Graph[N, ND, E, ED],
        get_weight: Callable[[ED], float]
) -> float:
    ret = 0.0
    for e in g.get_edges():
        e_data = g.get_edge_data(e)
        ret += get_weight(e_data)
    return ret
```