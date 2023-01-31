`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardSplitGraph.py](ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardSplitGraph.py) (lines 14 to 92):`{bm-enable-all}`

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
    # Isolate right-hand side and compute
    f_exploded_rhs = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    remove_before_node(f_exploded_rhs, f_exploded_n_id, hmm, hmm_source_n_id, hmm_sink_n_id)
    f_exploded_rhs_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded_rhs, emitted_seq)
    # Multiply to determine SINK value of the unsplit isolated exploded graph.
    f_exploded_sink_weight = f_exploded_lhs_sink_weight * f_exploded_rhs_sink_weight
    # Return
    return (f_exploded_lhs, f_exploded_lhs_sink_weight),\
           (f_exploded_rhs, f_exploded_rhs_sink_weight),\
           f_exploded_sink_weight


def remove_after_node(
        f_exploded: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        f_exploded_n_id: FORWARD_EXPLODED_NODE_ID,
        hmm_sink_n_id: STATE
):
    emitted_seq_idx_of_interest, hidden_state_of_interest = f_exploded_n_id
    for f_exploded_test_n_id in set(f_exploded.get_nodes()):
        emitted_seq_idx, hmm_n_id = f_exploded_test_n_id
        if (emitted_seq_idx == emitted_seq_idx_of_interest and hmm_n_id != hidden_state_of_interest)\
                or emitted_seq_idx > emitted_seq_idx_of_interest\
                or hmm_n_id == hmm_sink_n_id:
            delete_exploded_n_id = emitted_seq_idx, hmm_n_id
            f_exploded.delete_node(delete_exploded_n_id)
    # By deleting emitting hidden states in emitted_seq_idx_of_interest but not deleting non-emitting hidden states,
    # those non-emitting hidden states may have been orphaned (they've been disconnected from the main graph). Attempt
    # to clean them up here.
    filtered = True
    while filtered:
        filtered = False
        for f_exploded_test_n_id in set(f_exploded.get_root_nodes()):
            emitted_seq_idx, hmm_n_id = f_exploded_test_n_id
            if emitted_seq_idx == emitted_seq_idx_of_interest and f_exploded_n_id != f_exploded_test_n_id:
                f_exploded.delete_node(f_exploded_test_n_id)
                filtered = True


def remove_before_node(
        f_exploded: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        f_exploded_n_id: FORWARD_EXPLODED_NODE_ID,
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE
):
    emitted_seq_idx_of_interest, hidden_state_of_interest = f_exploded_n_id
    for f_exploded_test_n_id in set(f_exploded.get_nodes()):
        emitted_seq_idx, hmm_n_id = f_exploded_test_n_id
        if (emitted_seq_idx < emitted_seq_idx_of_interest and hmm_n_id != hmm_sink_n_id)\
                or (emitted_seq_idx == emitted_seq_idx_of_interest and hmm_n_id != hidden_state_of_interest and
                    hmm.get_node_data(hmm_n_id).is_emittable())\
                or hmm_n_id == hmm_source_n_id:
            delete_exploded_n_id = emitted_seq_idx, hmm_n_id
            f_exploded.delete_node(delete_exploded_n_id)
    # By deleting emitting hidden states in emitted_seq_idx_of_interest but not deleting non-emitting hidden states,
    # those non-emitting hidden states may have been orphaned (they've been disconnected from the main graph). Attempt
    # to clean them up here.
    filtered = True
    while filtered:
        filtered = False
        for f_exploded_test_n_id in set(f_exploded.get_root_nodes()):
            emitted_seq_idx, hmm_n_id = f_exploded_test_n_id
            if emitted_seq_idx == emitted_seq_idx_of_interest and f_exploded_n_id != f_exploded_test_n_id:
                f_exploded.delete_node(f_exploded_test_n_id)
                filtered = True
```