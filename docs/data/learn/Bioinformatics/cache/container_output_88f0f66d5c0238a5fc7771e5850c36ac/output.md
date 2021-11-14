`{bm-disable-all}`[ch7_code/src/sequence_phylogeny/SmallParsimony.py](ch7_code/src/sequence_phylogeny/SmallParsimony.py) (lines 53 to 145):`{bm-enable-all}`

```python
def populate_distance_sets(
        tree: Graph[N, ND, E, ED],
        seq_length: int,
        get_sequence: Callable[[N], str],
        set_sequence: Callable[[N, str], None],
        get_dist_set: Callable[
            [
                N,   # node
                int  # index within N's sequence
            ],
            dict[str, float]
        ],
        set_dist_set: Callable[
            [
                N,    # node
                int,  # index within N's sequence
                dict[str, float]
            ],
            None
        ],
        dist_metric: Callable[[str, str], float],
        root: Optional[N] = None,
        elem_types: str = 'ACTG'
) -> None:
    neighbours_unprocessed = Counter()
    for n in tree.get_nodes():
        neighbours_unprocessed[n] = tree.get_degree(n)
    leaf_nodes = {n for n, c in neighbours_unprocessed.items() if c == 1}
    internal_nodes = {n for n, c in neighbours_unprocessed.items() if c > 1}

    # Pick an internal node an treat it as a "root" by faking it having an
    # input. This will make it so that it gets processed last.
    if root is None:
        root = next(iter(internal_nodes))
    assert root in neighbours_unprocessed
    neighbours_unprocessed[root] += 1

    # Build dist sets for leaf nodes
    for n in leaf_nodes:
        # Build and set dist set for each element
        seq = get_sequence(n)
        for idx, elem in enumerate(seq):
            dist_set = distance_for_leaf_element_types(elem, elem_types)
            set_dist_set(n, idx, dist_set)
        # Decrement waiting count for upstream neighbour
        for edge in tree.get_outputs(n):
            n_upstream = tree.get_edge_end(edge, n)
            neighbours_unprocessed[n_upstream] -= 1
        # Remove from pending nodes
        neighbours_unprocessed.pop(n)

    # Build dist sets for internal nodes (walking up from leaf nodes)
    while True:
        # Get next node ready to be processed
        ready = {n for n, c in neighbours_unprocessed.items() if c == 1}
        if not ready:
            break
        n = ready.pop()
        # For each index, pull distance sets for outputs of n (that have them) and
        # use them to build a distance set for n.
        for i in range(seq_length):
            downstream_dist_sets = []
            for edge in tree.get_outputs(n):
                n_downstream = tree.get_edge_end(edge, n)
                if n_downstream in neighbours_unprocessed:
                    continue  # Skip -- this is actually upstream rather than downstream
                dist_set = get_dist_set(n_downstream, i)
                downstream_dist_sets.append(dist_set)
            dist_set = distance_for_internal_element_types(
                downstream_dist_sets,
                dist_metric,
                elem_types
            )
            set_dist_set(n, i, dist_set)
        # Mark neighbours as processed
        for edge in tree.get_outputs(n):
            n_upstream = tree.get_edge_end(edge, n)
            if n_upstream in neighbours_unprocessed:
                neighbours_unprocessed[n_upstream] -= 1
        # Remove from pending nodes
        neighbours_unprocessed.pop(n)

    # Set sequences for internal nodes based on dist sets
    for n in internal_nodes:
        seq = ''
        for i in range(seq_length):
            elem, _ = min(
                ((elem, dist) for elem, dist in get_dist_set(n, i).items()),
                key=lambda x: x[1]  # sort on dist
            )
            seq += elem
        set_sequence(n, seq)
```