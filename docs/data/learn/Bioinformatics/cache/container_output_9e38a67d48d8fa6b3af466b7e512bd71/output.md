`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_ForwardBackwardFullGraph.py](ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_ForwardBackwardFullGraph.py) (lines 145 to 180):`{bm-enable-all}`

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
    probs = {}
    for f_exploded_e_id in f_exploded.get_edges():
        f_exploded_from_n_id, f_exploded_to_n_id = f_exploded_e_id
        # Get node weights
        f = f_exploded.get_node_data(f_exploded_from_n_id)
        b_exploded_n_count = b_exploded_n_counter[f_exploded_to_n_id] + 1
        b = 0
        for i in range(b_exploded_n_count):
            b_exploded_n_id = f_exploded_to_n_id, i
            b += b_exploded.get_node_data(b_exploded_n_id)
        # Get transition probability of edge connecting gap. In certain cases, the SINK node may exist in the HMM. Here
        # we check that the transition exists in the HMM. If it does, we use the transition prob. If it doesn't but it's
        # the SINK node, it's assumed to have a 100% transition probability.
        f_exploded_sink_n_id = f_exploded.get_leaf_node()
        f_exploded_from_n_emissions_idx, hmm_from_n_id = f_exploded_from_n_id
        f_exploded_to_n_emission_idx, hmm_to_n_id = f_exploded_to_n_id
        f_exploded_middle_sink_weight = get_edge_probability(hmm, hmm_from_n_id, hmm_to_n_id, emitted_seq,
                                                             f_exploded_to_n_emission_idx)
        # Calculate probability and return
        prob = f * f_exploded_middle_sink_weight * b
        probs[f_exploded_e_id] = prob
    return f_exploded, b_exploded, probs
```