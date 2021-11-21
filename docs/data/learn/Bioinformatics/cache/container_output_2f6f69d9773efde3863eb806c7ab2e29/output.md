`{bm-disable-all}`[ch7_code/src/sequence_phylogeny/NearestNeighbourInterchange.py](ch7_code/src/sequence_phylogeny/NearestNeighbourInterchange.py) (lines 114 to 141):`{bm-enable-all}`

```python
def parsimony_score(
        tree: Graph[N, ND, E, ED],
        seq_length: int,
        get_dist_set: Callable[
            [
                N,  # node
                int  # index within N's sequence
            ],
            dict[str, float]
        ],
        set_edge_score: Callable[[E, float], None],
        dist_metric: Callable[[str, str], float]
) -> float:
    total_score = 0.0
    edges = set(tree.get_edges())  # iterator to set -- avoids concurrent modification bug
    for e in edges:
        n1, n2 = tree.get_edge_ends(e)
        e_score = 0.0
        for idx in range(seq_length):
            n1_ds = get_dist_set(n1, idx)
            n2_ds = get_dist_set(n2, idx)
            n1_elem = min(n1_ds, key=lambda k: n1_ds[k])
            n2_elem = min(n2_ds, key=lambda k: n2_ds[k])
            e_score += dist_metric(n1_elem, n2_elem)
        set_edge_score(e, e_score)
        total_score += e_score
    return total_score
```