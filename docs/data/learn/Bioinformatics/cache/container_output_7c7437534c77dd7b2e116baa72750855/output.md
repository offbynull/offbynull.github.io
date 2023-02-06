`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_ForwardBackwardSplitGraph.py](ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_ForwardBackwardSplitGraph.py) (lines 19 to 51):`{bm-enable-all}`

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
    # Forward compute left-hand side
    f_exploded_lhs = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    f_exploded_from_n_id = from_emission_idx, from_hidden_state
    remove_after_node(f_exploded_lhs, f_exploded_from_n_id)
    f_exploded_lhs_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded_lhs, emitted_seq)
    # Backward compute right-hand side
    f_exploded_rhs = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    f_exploded_rhs_to_n_id = (-1 if to_hidden_state == hmm_sink_n_id else from_emission_idx + 1), to_hidden_state
    remove_before_node(f_exploded_rhs, f_exploded_rhs_to_n_id)
    b_exploded_rhs, _ = backward_explode(hmm, f_exploded_rhs)
    b_exploded_rhs_source_weight = backward_exploded_hmm_calculation(hmm, b_exploded_rhs, emitted_seq)
    # Forward compute middle side (this is just the probability of the edge itself)
    _, hmm_from_n_id = f_exploded_from_n_id
    f_exploded_to_n_emission_idx, hmm_to_n_id = f_exploded_rhs_to_n_id
    f_exploded_middle_sink_weight = get_edge_probability(hmm, hmm_from_n_id, hmm_to_n_id, emitted_seq,
                                                         f_exploded_to_n_emission_idx)
    # Multiply to determine SINK value of the unsplit isolated exploded graph.
    f_exploded_sink_weight = f_exploded_lhs_sink_weight * f_exploded_middle_sink_weight * b_exploded_rhs_source_weight
    # Return
    return (f_exploded_lhs, f_exploded_lhs_sink_weight),\
           (b_exploded_rhs, b_exploded_rhs_source_weight),\
           f_exploded_middle_sink_weight,\
           f_exploded_sink_weight
```