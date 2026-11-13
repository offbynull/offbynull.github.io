`{bm-disable-all}`[ch10_code/src/hmm/CertaintyOfEmittedSequenceTravelingThroughHiddenPathEdge.py](ch10_code/src/hmm/CertaintyOfEmittedSequenceTravelingThroughHiddenPathEdge.py) (lines 15 to 28):`{bm-enable-all}`

```python
def edge_certainties(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL]
):
    f_exploded, b_exploded, filtered_probs = all_emission_probabilities(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    f_exploded_sink_n_id = f_exploded.get_leaf_node()
    unfiltered_prob = f_exploded.get_node_data(f_exploded_sink_n_id)
    certainty = {}
    for f_exploded_n_id, prob in filtered_probs.items():
        certainty[f_exploded_n_id] = prob / unfiltered_prob
    return f_exploded, b_exploded, certainty
```