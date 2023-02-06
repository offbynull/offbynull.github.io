`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_ForwardBackwardFullGraph.py](ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_ForwardBackwardFullGraph.py) (lines 17 to 48):`{bm-enable-all}`

```python
def emission_probability_single(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        from_emission_idx: int,
        from_hidden_state: STATE,
        to_hidden_state: STATE
):
    f_exploded_from_n_id = from_emission_idx, from_hidden_state
    f_exploded_to_n_id = (-1 if to_hidden_state == hmm_sink_n_id else from_emission_idx + 1), to_hidden_state
    # Left-hand side forward computation
    f_exploded = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    forward_exploded_hmm_calculation(hmm, f_exploded, emitted_seq)
    f = f_exploded.get_node_data(f_exploded_from_n_id)
    # Right-hand side backward computation
    b_exploded, b_exploded_n_counter = backward_explode(hmm, f_exploded)
    backward_exploded_hmm_calculation(hmm, b_exploded, emitted_seq)
    b_exploded_n_count = b_exploded_n_counter[f_exploded_to_n_id] + 1
    b = 0
    for i in range(b_exploded_n_count):
        b_exploded_n_id = f_exploded_to_n_id, i
        b += b_exploded.get_node_data(b_exploded_n_id)
    # Forward compute middle side (this is just the probability of the edge itself)
    _, hmm_from_n_id = f_exploded_from_n_id
    f_exploded_to_n_emission_idx, hmm_to_n_id = f_exploded_to_n_id
    f_exploded_middle_sink_weight = get_edge_probability(hmm, hmm_from_n_id, hmm_to_n_id, emitted_seq,
                                                         f_exploded_to_n_emission_idx)
    # Calculate probability and return
    prob = f * f_exploded_middle_sink_weight * b
    return (f_exploded, f), (b_exploded, b), f_exploded_middle_sink_weight, prob
```