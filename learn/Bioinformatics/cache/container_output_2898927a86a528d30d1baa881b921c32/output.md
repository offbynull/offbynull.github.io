`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardBackwardFullGraph.py](ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardBackwardFullGraph.py) (lines 169 to 196):`{bm-enable-all}`

```python
def all_emission_probabilities(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL]
):
    # Left-hand side forward computation
    f_exploded = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    forward_exploded_hmm_calculation(hmm, f_exploded, emitted_seq)
    # Right-hand side backward computation
    b_exploded, b_exploded_n_counter = backward_explode(hmm, f_exploded)
    backward_exploded_hmm_calculation(hmm, b_exploded, emitted_seq)
    # Calculate ALL probabilities
    f_exploded_n_ids = set(f_exploded.get_nodes())
    f_exploded_n_ids.remove(f_exploded.get_root_node())
    f_exploded_n_ids.remove(f_exploded.get_leaf_node())
    probs = {}
    for f_exploded_n_id in f_exploded_n_ids:
        f = f_exploded.get_node_data(f_exploded_n_id)
        b_exploded_n_count = b_exploded_n_counter[f_exploded_n_id] + 1
        b = 0
        for i in range(b_exploded_n_count):
            b_exploded_n_id = f_exploded_n_id, i
            b += b_exploded.get_node_data(b_exploded_n_id)
        prob = f * b
        probs[f_exploded_n_id] = prob
    return f_exploded, b_exploded, probs
```