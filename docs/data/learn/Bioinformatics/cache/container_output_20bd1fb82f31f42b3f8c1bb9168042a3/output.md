`{bm-disable-all}`[ch10_code/src/hmm/MostProbableEmittedSequence_Graph.py](ch10_code/src/hmm/MostProbableEmittedSequence_Graph.py) (lines 501 to 532):`{bm-enable-all}`

```python
def backtrack(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        exploded: Graph[EXPLODED_NODE_ID, Any, EXPLODED_EDGE_ID, float]
) -> list[SYMBOL]:
    exploded_source_n_id = exploded.get_root_node()
    exploded_sink_n_id = exploded.get_leaf_node()
    _, hmm_sink_n_id, _ = exploded_sink_n_id
    exploded_to_n_id = exploded_sink_n_id
    exploded_last_emission_idx, _, _ = exploded_to_n_id
    emitted_seq = []
    while exploded_to_n_id != exploded_source_n_id:
        _, hmm_to_n_id, exploded_to_layer = exploded_to_n_id
        # Add exploded_to_n_id's layer to the emitted sequence if it's an emittable node. The layer is represented by
        # the symbol for that layer, so the symbol is being added to the emitted sequence. The SINK node may not exist
        # in the HMM, so if exploded_to_n_id is the SINK node, filter it out of test (SINK node will never emit a symbol
        # and isn't part of a layer).
        if hmm_to_n_id != hmm_sink_n_id and hmm.get_node_data(hmm_to_n_id).is_emittable():
            emitted_seq.insert(0, exploded_to_layer)
        backtracking_layer, _ = exploded.get_node_data(exploded_to_n_id)
        # The backtracking symbol is the layer this came from. Collect all nodes in that layer that have edges to
        # exploded_to_n_id.
        exploded_from_n_id_and_weights = []
        for _, exploded_from_n_id, _, _ in exploded.get_inputs_full(exploded_to_n_id):
            _, _, exploded_from_layer = exploded_from_n_id
            if exploded_from_layer != backtracking_layer:
                continue
            _, weight = exploded.get_node_data(exploded_from_n_id)
            exploded_from_n_id_and_weights.append((weight, exploded_from_n_id))
        # Of those collected nodes, the one with the maximum weight is the one that gets selected.
        _, exploded_to_n_id = max(exploded_from_n_id_and_weights, key=lambda x: x[0])
    return emitted_seq
```