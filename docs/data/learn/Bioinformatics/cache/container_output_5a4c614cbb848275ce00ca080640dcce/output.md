`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_ForwardGraph.py](ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_ForwardGraph.py) (lines 15 to 55):`{bm-enable-all}`

```python
def emission_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        from_emission_idx: int,
        from_hidden_state: STATE,
        to_hidden_state: STATE
):
    f_exploded = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    filter_at_emission_idx(f_exploded, from_emission_idx, from_hidden_state, to_hidden_state)
    f_exploded_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded, emitted_seq)
    return f_exploded, f_exploded_sink_weight


def filter_at_emission_idx(
        f_exploded: Graph[FORWARD_EXPLODED_NODE_ID, Any, FORWARD_EXPLODED_EDGE_ID, Any],
        from_emission_idx: int,
        from_hidden_state: STATE,
        to_hidden_state: STATE
):
    for f_exploded_transition in set(f_exploded.get_edges()):
        f_exploded_from_n_id, f_exploded_to_n_id = f_exploded_transition
        f_exploded_from_n_emission_idx, hmm_from_n_id = f_exploded_from_n_id
        f_exploded_to_n_emission_idx, hmm_to_n_id = f_exploded_to_n_id
        if f_exploded_from_n_emission_idx == from_emission_idx:
            if not hmm_from_n_id == from_hidden_state and f_exploded.has_node(f_exploded_from_n_id):
                f_exploded.delete_node(f_exploded_from_n_id)
            if not hmm_to_n_id == to_hidden_state and f_exploded.has_node(f_exploded_to_n_id):
                f_exploded.delete_node(f_exploded_to_n_id)
    # Non-emitting hidden states may have been orphaned (they've been disconnected from the main graph). Attempt to
    # clean them up here.
    filtered = True
    while filtered:
        filtered = False
        for f_exploded_test_n_id in set(f_exploded.get_root_nodes()):
            emission_idx, hmm_n_id = f_exploded_test_n_id
            if emission_idx == from_emission_idx or emission_idx == from_emission_idx + 1:
                f_exploded.delete_node(f_exploded_test_n_id)
                filtered = True
```