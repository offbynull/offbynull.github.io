`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_ForwardSplitGraph.py](ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_ForwardSplitGraph.py) (lines 130 to 181):`{bm-enable-all}`

```python
def emission_probability_three_split(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        from_emission_idx: int,
        from_hidden_state: STATE,
        to_hidden_state: STATE
):
    # Isolate left-hand side and compute
    f_exploded_lhs = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    f_exploded_from_n_id = from_emission_idx, from_hidden_state
    remove_after_node(f_exploded_lhs, f_exploded_from_n_id)
    f_exploded_lhs_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded_lhs, emitted_seq)
    # Isolate right-hand side and compute
    f_exploded_rhs = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    f_exploded_rhs_to_n_id = (-1 if to_hidden_state == hmm_sink_n_id else from_emission_idx + 1), to_hidden_state
    remove_before_node(f_exploded_rhs, f_exploded_rhs_to_n_id)
    f_exploded_rhs_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded_rhs, emitted_seq)
    # Isolate middle-hand side and compute
    _, hmm_from_n_id = f_exploded_from_n_id
    f_exploded_to_n_emission_idx, hmm_to_n_id = f_exploded_rhs_to_n_id
    f_exploded_middle_sink_weight = get_edge_probability(hmm, hmm_from_n_id, hmm_to_n_id, emitted_seq,
                                                         f_exploded_to_n_emission_idx)
    # Multiply to determine SINK value of the unsplit isolated exploded graph.
    f_exploded_sink_weight = f_exploded_lhs_sink_weight * f_exploded_middle_sink_weight * f_exploded_rhs_sink_weight
    # Return
    return (f_exploded_lhs, f_exploded_lhs_sink_weight),\
           (f_exploded_rhs, f_exploded_rhs_sink_weight),\
           f_exploded_middle_sink_weight,\
           f_exploded_sink_weight


def get_edge_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_from_n_id: STATE,
        hmm_to_n_id: STATE,
        emitted_seq: list[SYMBOL],
        emission_idx: int
) -> float:
    symbol = emitted_seq[emission_idx]
    if hmm.has_node(hmm_to_n_id) and hmm.get_node_data(hmm_to_n_id).is_emittable():
        symbol_emission_prob = hmm.get_node_data(hmm_to_n_id).get_symbol_emission_probability(symbol)
    else:
        symbol_emission_prob = 1.0  # No emission - setting to 1.0 means it has no effect in multiplication later on
    transition = hmm_from_n_id, hmm_to_n_id
    if hmm.has_edge(transition):
        transition_prob = hmm.get_edge_data(transition).get_transition_probability()
    else:
        transition_prob = 1.0  # Setting to 1.0 means it always happens
    return transition_prob * symbol_emission_prob
```