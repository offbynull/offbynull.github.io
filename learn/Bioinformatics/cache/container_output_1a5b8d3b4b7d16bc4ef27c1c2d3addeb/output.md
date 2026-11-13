`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_ForwardSplitGraph.py](ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_ForwardSplitGraph.py) (lines 18 to 44):`{bm-enable-all}`

```python
def emission_probability_two_split(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        from_emission_idx: int,
        from_hidden_state: STATE,
        to_hidden_state: STATE
):
    f_exploded_n_id = from_emission_idx, from_hidden_state
    # Isolate left-hand side and compute
    f_exploded_lhs = forward_explode_hmm_and_isolate_edge(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq,
                                                          from_emission_idx, from_hidden_state, to_hidden_state)
    remove_after_node(f_exploded_lhs, f_exploded_n_id)
    f_exploded_lhs_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded_lhs, emitted_seq)
    # Isolate right-hand side and compute
    f_exploded_rhs = forward_explode_hmm_and_isolate_edge(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq,
                                                          from_emission_idx, from_hidden_state, to_hidden_state)
    remove_before_node(f_exploded_rhs, f_exploded_n_id)
    f_exploded_rhs_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded_rhs, emitted_seq)
    # Multiply to determine SINK value of the unsplit isolated exploded graph.
    f_exploded_sink_weight = f_exploded_lhs_sink_weight * f_exploded_rhs_sink_weight
    # Return
    return (f_exploded_lhs, f_exploded_lhs_sink_weight),\
           (f_exploded_rhs, f_exploded_rhs_sink_weight),\
           f_exploded_sink_weight
```