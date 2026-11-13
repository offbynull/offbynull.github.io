`{bm-disable-all}`[ch10_code/src/hmm/MostProbableEmittedSequence_ForwardGraph.py](ch10_code/src/hmm/MostProbableEmittedSequence_ForwardGraph.py) (lines 13 to 114):`{bm-enable-all}`

```python
LAYERED_FORWARD_EXPLODED_NODE_ID = tuple[int, STATE, SYMBOL | None]
LAYERED_FORWARD_EXPLODED_EDGE_ID = tuple[LAYERED_FORWARD_EXPLODED_NODE_ID, LAYERED_FORWARD_EXPLODED_NODE_ID]


def layer_explode_hmm(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        symbols: set[SYMBOL],
        emission_len: int
) -> Graph[LAYERED_FORWARD_EXPLODED_NODE_ID, Any, LAYERED_FORWARD_EXPLODED_EDGE_ID, Any]:
    f_exploded = Graph()
    # Add exploded source node.
    f_exploded_source_n_id = -1, hmm_source_n_id, None
    f_exploded.insert_node(f_exploded_source_n_id)
    # Explode out HMM into new graph.
    f_exploded_from_n_emissions_idx = -1
    f_exploded_from_n_ids = {f_exploded_source_n_id}
    f_exploded_to_n_emissions_idx = 0
    f_exploded_to_n_ids_emitting = set()
    f_exploded_to_n_ids_non_emitting = set()
    while f_exploded_from_n_ids and f_exploded_to_n_emissions_idx < emission_len:
        f_exploded_to_n_ids_emitting = set()
        f_exploded_to_n_ids_non_emitting = set()
        while f_exploded_from_n_ids:
            f_exploded_from_n_id = f_exploded_from_n_ids.pop()
            _, hmm_from_n_id, f_exploded_from_symbol = f_exploded_from_n_id
            for f_exploded_to_n_symbol in symbols:
                for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
                    hmm_to_n_emittable = hmm.get_node_data(hmm_to_n_id).is_emittable()
                    if hmm_to_n_emittable:
                        f_exploded_to_n_id = f_exploded_to_n_emissions_idx, hmm_to_n_id, f_exploded_to_n_symbol
                        connect_exploded_nodes(
                            f_exploded,
                            f_exploded_from_n_id,
                            f_exploded_to_n_id,
                            None
                        )
                        f_exploded_to_n_ids_emitting.add(f_exploded_to_n_id)
                    else:
                        f_exploded_to_n_id = f_exploded_from_n_emissions_idx, hmm_to_n_id, f_exploded_to_n_symbol
                        to_n_existed = connect_exploded_nodes(
                            f_exploded,
                            f_exploded_from_n_id,
                            f_exploded_to_n_id,
                            None
                        )
                        if not to_n_existed:
                            f_exploded_from_n_ids.add(f_exploded_to_n_id)
                        f_exploded_to_n_ids_non_emitting.add(f_exploded_to_n_id)
        f_exploded_from_n_ids = f_exploded_to_n_ids_emitting
        f_exploded_from_n_emissions_idx += 1
        f_exploded_to_n_emissions_idx += 1
    # Ensure all emitted symbols were consumed when exploding out to exploded.
    assert f_exploded_to_n_emissions_idx == emission_len
    # Explode out the non-emitting hidden states of the final last emission index (does not happen in the above loop).
    f_exploded_to_n_ids_non_emitting = set()
    f_exploded_from_n_ids = f_exploded_to_n_ids_emitting.copy()
    while f_exploded_from_n_ids:
        f_exploded_from_n_id = f_exploded_from_n_ids.pop()
        _, hmm_from_n_id, f_exploded_from_symbol = f_exploded_from_n_id
        for f_exploded_to_n_symbol in symbols:
            for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
                hmm_to_n_emittable = hmm.get_node_data(hmm_to_n_id).is_emittable()
                if hmm_to_n_emittable:
                    continue
                f_exploded_to_n_id = f_exploded_from_n_emissions_idx, hmm_to_n_id, f_exploded_to_n_symbol
                connect_exploded_nodes(
                    f_exploded,
                    f_exploded_from_n_id,
                    f_exploded_to_n_id,
                    None
                )
                f_exploded_to_n_ids_non_emitting.add(f_exploded_to_n_id)
                f_exploded_from_n_ids.add(f_exploded_to_n_id)
    # Add exploded sink node.
    f_exploded_to_n_id = -1, hmm_sink_n_id, None
    for f_exploded_from_n_id in f_exploded_to_n_ids_emitting | f_exploded_to_n_ids_non_emitting:
        connect_exploded_nodes(f_exploded, f_exploded_from_n_id, f_exploded_to_n_id, None)
    return f_exploded


def connect_exploded_nodes(
        f_exploded: Graph[LAYERED_FORWARD_EXPLODED_NODE_ID, Any, LAYERED_FORWARD_EXPLODED_EDGE_ID, float],
        f_exploded_from_n_id: LAYERED_FORWARD_EXPLODED_NODE_ID,
        f_exploded_to_n_id: LAYERED_FORWARD_EXPLODED_NODE_ID,
        weight: Any
) -> bool:
    to_n_existed = True
    if not f_exploded.has_node(f_exploded_to_n_id):
        f_exploded.insert_node(f_exploded_to_n_id)
        to_n_existed = False
    f_exploded_e_weight = weight
    f_exploded_e_id = f_exploded_from_n_id, f_exploded_to_n_id
    f_exploded.insert_edge(
        f_exploded_e_id,
        f_exploded_from_n_id,
        f_exploded_to_n_id,
        f_exploded_e_weight
    )
    return to_n_existed
```