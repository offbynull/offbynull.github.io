`{bm-disable-all}`[ch10_code/src/hmm/MostProbableEmittedSequence_Graph.py](ch10_code/src/hmm/MostProbableEmittedSequence_Graph.py) (lines 147 to 248):`{bm-enable-all}`

```python
EXPLODED_NODE_ID = tuple[int, STATE, SYMBOL | None]
EXPLODED_EDGE_ID = tuple[EXPLODED_NODE_ID, EXPLODED_NODE_ID]


def explode_hmm(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        symbols: set[SYMBOL],
        emission_len: int
) -> Graph[EXPLODED_NODE_ID, Any, EXPLODED_EDGE_ID, Any]:
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
                    hmm_to_n_emittable = hmm.get_node_data(hmm_to_n_id).is_emittable()
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
                hmm_to_n_emittable = hmm.get_node_data(hmm_to_n_id).is_emittable()
                if hmm_to_n_emittable:
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
        exploded: Graph[EXPLODED_NODE_ID, Any, EXPLODED_EDGE_ID, float],
        exploded_from_n_id: EXPLODED_NODE_ID,
        exploded_to_n_id: EXPLODED_NODE_ID,
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