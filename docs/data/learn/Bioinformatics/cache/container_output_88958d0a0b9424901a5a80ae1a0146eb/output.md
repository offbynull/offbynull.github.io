`{bm-disable-all}`[ch7_code/src/sequence_phylogeny/NearestNeighbourInterchange.py](ch7_code/src/sequence_phylogeny/NearestNeighbourInterchange.py) (lines 145 to 250):`{bm-enable-all}`

```python
def nn_interchange(
        tree: Graph[N, ND, E, ED],
        root: N,
        seq_length: int,
        get_sequence: Callable[[N], str],
        set_sequence: Callable[[N, str], None],
        get_dist_set: Callable[
            [
                N,  # node
                int  # index within N's sequence
            ],
            dict[str, float]
        ],
        set_dist_set: Callable[
            [
                N,  # node
                int,  # index within N's sequence
                dict[str, float]
            ],
            None
        ],
        dist_metric: Callable[[str, str], float],
        set_edge_score: Callable[[E, float], None],
        elem_types: str = 'ACTG',
        update_callback: Optional[Callable[[Graph, float], None]] = None
) -> tuple[float, float]:
    input_score = None
    output_score = None
    while True:
        populate_distance_sets(
            tree,
            root,
            seq_length,
            get_sequence,
            set_sequence,
            get_dist_set,
            set_dist_set,
            dist_metric,
            elem_types
        )
        orig_score = parsimony_score(
            tree,
            seq_length,
            get_dist_set,
            set_edge_score,
            dist_metric
        )
        if input_score is None:
            input_score = orig_score
        output_score = orig_score
        if update_callback is not None:
            update_callback(tree, output_score)  # notify caller that the graph updated
        swap_scores = []
        edges = set(tree.get_edges())  # bug -- avoids concurrent modification problems
        for edge in edges:
            # is it a limb? if so, skip it -- we want internal edges only
            n1, n2 = tree.get_edge_ends(edge)
            if tree.get_degree(n1) == 1 or tree.get_degree(n2) == 1:
                continue
            # get all possible nn swaps for this internal edge
            options = list_nn_swap_options(tree, edge)
            # for each possible swap...
            for swapped_side1, swapped_side2 in options:
                # swap
                orig_side1, orig_side2 = nn_swap(
                    tree,
                    edge,
                    swapped_side1,
                    swapped_side2
                )
                # small parsimony
                populate_distance_sets(
                    tree,
                    root,
                    seq_length,
                    get_sequence,
                    set_sequence,
                    get_dist_set,
                    set_dist_set,
                    dist_metric,
                    elem_types
                )
                # score and store
                score = parsimony_score(
                    tree,
                    seq_length,
                    get_dist_set,
                    set_edge_score,
                    dist_metric
                )
                swap_scores.append((score, edge, swapped_side1, swapped_side2))
                # unswap (back to original tree)
                nn_swap(
                    tree,
                    edge,
                    orig_side1,
                    orig_side2
                )
        # if swap producing the lowest parsimony score is lower than original, apply that
        # swap and try again, otherwise we're finished
        score, edge, side1, side2 = min(swap_scores, key=lambda x: x[0])
        if score >= orig_score:
            return input_score, output_score
        else:
            nn_swap(tree, edge, side1, side2)
```