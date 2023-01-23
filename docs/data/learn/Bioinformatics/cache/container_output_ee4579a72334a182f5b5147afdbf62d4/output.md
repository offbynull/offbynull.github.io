`{bm-disable-all}`[ch10_code/src/hmm/MostProbableEmittedSequence_Graph.py](ch10_code/src/hmm/MostProbableEmittedSequence_Graph.py) (lines 39 to 137):`{bm-enable-all}`

```python
def explode_hmm(
        hmm: Graph[N, ND, E, ED],
        hmm_source_n_id: N,
        hmm_sink_n_id: N,
        symbols: set[SYMBOL],
        emission_len: int,
        get_node_emittable: Callable[[Graph[N, ND, E, ED], STATE], bool],
) -> Graph[tuple[int, N, SYMBOL], Any, tuple[N, N], Any]:
    exploded = Graph()
    # Add exploded source node.
    exploded_source_n_id = -1, hmm_source_n_id, None
    exploded.insert_node(exploded_source_n_id)
    # Explode out HMM into new graph.
    exploded_from_n_emissions_idx = -1
    exploded_from_n_ids = {exploded_source_n_id}
    exploded_to_n_emissions_idx = 0
    exploded_to_n_ids_emitting = set()
    exploded_to_n_ids_non_emitting = set()
    while exploded_from_n_ids and exploded_to_n_emissions_idx < emission_len:
        exploded_to_n_ids_emitting = set()
        exploded_to_n_ids_non_emitting = set()
        while exploded_from_n_ids:
            exploded_from_n_id = exploded_from_n_ids.pop()
            _, hmm_from_n_id, exploded_from_symbol = exploded_from_n_id
            for exploded_to_n_symbol in symbols:
                for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
                    hmm_to_n_emittable = get_node_emittable(hmm, hmm_to_n_id)
                    if hmm_to_n_emittable:
                        exploded_to_n_id = exploded_to_n_emissions_idx, hmm_to_n_id, exploded_to_n_symbol
                        connect_exploded_nodes(
                            exploded,
                            exploded_from_n_id,
                            exploded_to_n_id,
                            None
                        )
                        exploded_to_n_ids_emitting.add(exploded_to_n_id)
                    else:
                        exploded_to_n_id = exploded_from_n_emissions_idx, hmm_to_n_id, exploded_to_n_symbol
                        to_n_existed = connect_exploded_nodes(
                            exploded,
                            exploded_from_n_id,
                            exploded_to_n_id,
                            None
                        )
                        if not to_n_existed:
                            exploded_from_n_ids.add(exploded_to_n_id)
                        exploded_to_n_ids_non_emitting.add(exploded_to_n_id)
        exploded_from_n_ids = exploded_to_n_ids_emitting
        exploded_from_n_emissions_idx += 1
        exploded_to_n_emissions_idx += 1
    # Ensure all emitted symbols were consumed when exploding out to exploded.
    assert exploded_to_n_emissions_idx == emission_len
    # Explode out the non-emitting hidden states of the final last emission index (does not happen in the above loop).
    exploded_to_n_ids_non_emitting = set()
    exploded_from_n_ids = exploded_to_n_ids_emitting.copy()
    while exploded_from_n_ids:
        exploded_from_n_id = exploded_from_n_ids.pop()
        _, hmm_from_n_id, exploded_from_symbol = exploded_from_n_id
        for exploded_to_n_symbol in symbols:
            for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
                hmm_to_n_emmitable = get_node_emittable(hmm, hmm_to_n_id)
                if hmm_to_n_emmitable:
                    continue
                exploded_to_n_id = exploded_from_n_emissions_idx, hmm_to_n_id, exploded_to_n_symbol
                connect_exploded_nodes(
                    exploded,
                    exploded_from_n_id,
                    exploded_to_n_id,
                    None
                )
                exploded_to_n_ids_non_emitting.add(exploded_to_n_id)
                exploded_from_n_ids.add(exploded_to_n_id)
    # Add exploded sink node.
    exploded_to_n_id = -1, hmm_sink_n_id, None
    for exploded_from_n_id in exploded_to_n_ids_emitting | exploded_to_n_ids_non_emitting:
        connect_exploded_nodes(exploded, exploded_from_n_id, exploded_to_n_id, None)
    return exploded


def connect_exploded_nodes(
        exploded: Graph[tuple[int, N], Any, tuple[N, N], Any],
        exploded_from_n_id: tuple[int, N, SYMBOL],
        exploded_to_n_id: tuple[int, N, SYMBOL],
        weight: Any
) -> bool:
    to_n_existed = True
    if not exploded.has_node(exploded_to_n_id):
        exploded.insert_node(exploded_to_n_id)
        to_n_existed = False
    exploded_e_weight = weight
    exploded_e_id = exploded_from_n_id, exploded_to_n_id
    exploded.insert_edge(
        exploded_e_id,
        exploded_from_n_id,
        exploded_to_n_id,
        exploded_e_weight
    )
    return to_n_existed
```