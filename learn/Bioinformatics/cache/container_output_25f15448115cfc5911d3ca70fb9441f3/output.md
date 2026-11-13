`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardBackwardFullGraph.py](ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardBackwardFullGraph.py) (lines 16 to 40):`{bm-enable-all}`

```python
def emission_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        emitted_seq_idx_of_interest: int,
        hidden_state_of_interest: STATE
):
    # Left-hand side forward computation
    f_exploded = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    forward_exploded_hmm_calculation(hmm, f_exploded, emitted_seq)
    f_exploded_n_id = emitted_seq_idx_of_interest, hidden_state_of_interest
    f = f_exploded.get_node_data(f_exploded_n_id)
    # Right-hand side backward computation
    b_exploded, b_exploded_n_counter = backward_explode(hmm, f_exploded)
    backward_exploded_hmm_calculation(hmm, b_exploded, emitted_seq)
    b_exploded_n_count = b_exploded_n_counter[f_exploded_n_id] + 1
    b = 0
    for i in range(b_exploded_n_count):
        b_exploded_n_id = f_exploded_n_id, i
        b += b_exploded.get_node_data(b_exploded_n_id)
    # Calculate probability and return
    prob = f * b
    return (f_exploded, f), (b_exploded, b), prob
```