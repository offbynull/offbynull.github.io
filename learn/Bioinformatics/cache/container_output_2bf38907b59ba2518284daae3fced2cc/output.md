`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_ForwardGraph.py](ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_ForwardGraph.py) (lines 17 to 65):`{bm-enable-all}`

```python
def emission_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        from_emission_idx: int,
        from_hidden_state: STATE,
        to_hidden_state: STATE
):
    f_exploded = forward_explode_hmm_and_isolate_edge(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq,
                                                      from_emission_idx, from_hidden_state, to_hidden_state)
    # Compute sink weight
    f_exploded_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded, emitted_seq)
    return f_exploded, f_exploded_sink_weight


def forward_explode_hmm_and_isolate_edge(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        from_emission_idx: int,
        from_hidden_state: STATE,
        to_hidden_state: STATE
):
    f_exploded = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    # Filter starting emission index to edge's starting node.
    f_exploded_keep_from_n_id = from_emission_idx, from_hidden_state
    filter_at_emission_idx(f_exploded, f_exploded_keep_from_n_id)
    # Filter ending emission index to edge's ending node.
    f_exploded_keep_to_n_id = (-1 if to_hidden_state == hmm_sink_n_id else from_emission_idx + 1), to_hidden_state
    filter_at_emission_idx(f_exploded, f_exploded_keep_to_n_id)
    # For the edge's ...
    #  * start node, keep that edge as its only outgoing edge.
    #  * ending node, keep that edge as its only incoming edge.
    for transition in f_exploded.get_outputs(f_exploded_keep_from_n_id):
        _, f_exploded_to_n_id = transition
        if f_exploded_to_n_id != f_exploded_keep_to_n_id:
            f_exploded.delete_edge(transition)
    for transition in f_exploded.get_inputs(f_exploded_keep_to_n_id):
        f_exploded_from_n_id, _ = transition
        if f_exploded_from_n_id != f_exploded_keep_from_n_id:
            f_exploded.delete_edge(transition)
    # By deleting nodes/edges, other nodes may have been orphaned (pointing to dead-ends or starting from dead-ends).
    # Delete those nodes such that there are no dead-ends.
    delete_dead_end_nodes(f_exploded, f_exploded_keep_from_n_id)
    # Return
    return f_exploded
```