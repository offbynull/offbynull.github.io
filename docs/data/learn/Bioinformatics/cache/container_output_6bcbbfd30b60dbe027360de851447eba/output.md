`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardSplitGraph.py](ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardSplitGraph.py) (lines 15 to 78):`{bm-enable-all}`

```python
def emission_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        emitted_seq_idx_of_interest: int,
        hidden_state_of_interest: STATE
):
    f_exploded_n_id = emitted_seq_idx_of_interest, hidden_state_of_interest
    # Isolate left-hand side and compute
    f_exploded_lhs = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    remove_after_node(f_exploded_lhs, f_exploded_n_id)
    f_exploded_lhs_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded_lhs, emitted_seq)
    # Isolate right-hand side and compute
    f_exploded_rhs = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    remove_before_node(f_exploded_rhs, f_exploded_n_id)
    f_exploded_rhs_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded_rhs, emitted_seq)
    # Multiply to determine SINK value of the unsplit isolated exploded graph.
    f_exploded_sink_weight = f_exploded_lhs_sink_weight * f_exploded_rhs_sink_weight
    # Return
    return (f_exploded_lhs, f_exploded_lhs_sink_weight),\
           (f_exploded_rhs, f_exploded_rhs_sink_weight),\
           f_exploded_sink_weight


def remove_after_node(
        f_exploded: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        f_exploded_keep_n_id: FORWARD_EXPLODED_NODE_ID
):
    # Filter emission index to f_exploded_keep_n_id
    filter_at_emission_idx(f_exploded, f_exploded_keep_n_id)
    # Walk forward to sink and remove everything after f_exploded_keep_n_id
    pending = {f_exploded_keep_n_id}
    visited = set()
    while pending:
        f_exploded_n_id = pending.pop()
        visited.add(f_exploded_n_id)
        for _, _, f_exploded_to_n_id, _ in f_exploded.get_outputs_full(f_exploded_n_id):
            if f_exploded_to_n_id not in visited:
                pending.add(f_exploded_to_n_id)
    visited.remove(f_exploded_keep_n_id)
    for f_exploded_n_id in visited:
        f_exploded.delete_node(f_exploded_n_id)


def remove_before_node(
        f_exploded: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        f_exploded_keep_n_id: FORWARD_EXPLODED_NODE_ID
):
    # Filter emission index to f_exploded_keep_n_id
    filter_at_emission_idx(f_exploded, f_exploded_keep_n_id)
    # Walk forward to sink and remove everything after f_exploded_keep_n_id
    pending = {f_exploded_keep_n_id}
    visited = set()
    while pending:
        f_exploded_n_id = pending.pop()
        visited.add(f_exploded_n_id)
        for _, f_exploded_from_n_id, _, _ in f_exploded.get_inputs_full(f_exploded_n_id):
            if f_exploded_from_n_id not in visited:
                pending.add(f_exploded_from_n_id)
    visited.remove(f_exploded_keep_n_id)
    for f_exploded_n_id in visited:
        f_exploded.delete_node(f_exploded_n_id)
```