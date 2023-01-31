`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardBackwardSplitGraph.py](ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardBackwardSplitGraph.py) (lines 202 to 277):`{bm-enable-all}`

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
    remove_after_node(f_exploded_lhs, f_exploded_n_id, hmm_sink_n_id)
    f_exploded_lhs_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded_lhs, emitted_seq)
    # Isolate right-hand side and compute BACKWARDS
    f_exploded_rhs = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    filter_at_emission_idx(hmm, f_exploded_rhs, emitted_seq_idx_of_interest, hidden_state_of_interest)
    remove_before_node(f_exploded_rhs, f_exploded_n_id, hmm, hmm_source_n_id, hmm_sink_n_id)
    b_exploded_rhs, _ = backward_explode(hmm, f_exploded_rhs)
    b_exploded_rhs_source_weight = backward_exploded_hmm_calculation(hmm, b_exploded_rhs, emitted_seq)
    # Multiply to determine SINK value of the unsplit isolated exploded graph.
    f_exploded_sink_weight = f_exploded_lhs_sink_weight * b_exploded_rhs_source_weight
    # Return
    return (f_exploded_lhs, f_exploded_lhs_sink_weight),\
           (b_exploded_rhs, b_exploded_rhs_source_weight),\
           f_exploded_sink_weight


def backward_exploded_hmm_calculation(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        b_exploded: Graph[BACKWARD_EXPLODED_NODE_ID, Any, BACKWARD_EXPLODED_EDGE_ID, Any],
        emitted_seq: list[SYMBOL]
):
    b_exploded_source_n_id = b_exploded.get_root_node()
    b_exploded_sink_n_id = b_exploded.get_leaf_node()
    (b_exploded_sink_n_emissions_idx, hmm_sink_n_id), _ = b_exploded_sink_n_id
    b_exploded.update_node_data(b_exploded_sink_n_id, 1.0)
    b_exploded_from_n_ids = set()
    add_ready_to_process_incoming_nodes(b_exploded, b_exploded_sink_n_id, b_exploded_from_n_ids)
    while b_exploded_from_n_ids:
        b_exploded_from_n_id = b_exploded_from_n_ids.pop()
        (_, hmm_from_n_id), _ = b_exploded_from_n_id
        b_exploded_from_backward_weight = 0.0
        for _, _, b_exploded_to_n_id, _ in b_exploded.get_outputs_full(b_exploded_from_n_id):
            b_exploded_to_backward_weight = b_exploded.get_node_data(b_exploded_to_n_id)
            (b_exploded_to_n_emissions_idx, hmm_to_n_id), _ = b_exploded_to_n_id
            # Determine symbol emission prob.
            symbol = emitted_seq[b_exploded_to_n_emissions_idx]
            if hmm.has_node(hmm_to_n_id) and hmm.get_node_data(hmm_to_n_id).is_emittable():
                symbol_emission_prob = hmm.get_node_data(hmm_to_n_id).get_symbol_emission_probability(symbol)
            else:
                symbol_emission_prob = 1.0  # No emission - setting to 1.0 means it has no effect in multiply later on
            # Determine transition prob.
            transition = hmm_from_n_id, hmm_to_n_id
            if hmm.has_edge(transition):
                transition_prob = hmm.get_edge_data(transition).get_transition_probability()
            else:
                transition_prob = 1.0  # Setting to 1.0 means it always happens
            b_exploded_from_backward_weight += b_exploded_to_backward_weight * transition_prob * symbol_emission_prob
        b_exploded.update_node_data(b_exploded_from_n_id, b_exploded_from_backward_weight)
        add_ready_to_process_incoming_nodes(b_exploded, b_exploded_from_n_id, b_exploded_from_n_ids)
    return b_exploded.get_node_data(b_exploded_source_n_id)


# Given a node in the exploded graph (exploded_n_from_id), look at each outgoing neighbours that it has
# (exploded_to_n_id). If that outgoing neighbour (exploded_to_n_id) has a "forward weight" set for all of its incoming
# neighbours, add it to the set of "ready_to_process" nodes.
def add_ready_to_process_incoming_nodes(
        backward_exploded: Graph[BACKWARD_EXPLODED_NODE_ID, Any, BACKWARD_EXPLODED_EDGE_ID, Any],
        backward_exploded_n_from_id: BACKWARD_EXPLODED_NODE_ID,
        ready_to_process_n_ids: set[BACKWARD_EXPLODED_NODE_ID]
):
    for _, exploded_from_n_id, _, _ in backward_exploded.get_inputs_full(backward_exploded_n_from_id):
        ready_to_process = all(backward_exploded.get_node_data(n) is not None for _, _, n, _ in backward_exploded.get_outputs_full(exploded_from_n_id))
        if ready_to_process:
            ready_to_process_n_ids.add(exploded_from_n_id)
```