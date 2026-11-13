`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardGraph.py](ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardGraph.py) (lines 15 to 96):`{bm-enable-all}`

```python
def emission_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        emitted_seq_idx_of_interest: int,
        hidden_state_of_interest: STATE
):
    f_exploded = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    f_exploded_keep_n_id = emitted_seq_idx_of_interest, hidden_state_of_interest
    filter_at_emission_idx(f_exploded, f_exploded_keep_n_id)
    f_exploded_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded, emitted_seq)
    return f_exploded, f_exploded_sink_weight


def filter_at_emission_idx(
        f_exploded: Graph[FORWARD_EXPLODED_NODE_ID, Any, FORWARD_EXPLODED_EDGE_ID, Any],
        f_exploded_keep_n_id: FORWARD_EXPLODED_NODE_ID
):
    f_exploded_keep_n_emission_idx, _ = f_exploded_keep_n_id
    f_exploded_keep_n_ids = get_connected_nodes_at_emission_idx(f_exploded, f_exploded_keep_n_id)
    for f_exploded_test_n_id in set(f_exploded.get_nodes()):
        f_exploded_test_n_emission_idx, _ = f_exploded_test_n_id
        if f_exploded_test_n_emission_idx == f_exploded_keep_n_emission_idx\
                and f_exploded_test_n_id not in f_exploded_keep_n_ids:
            f_exploded.delete_node(f_exploded_test_n_id)
    # By deleting nodes above, other nodes may have been orphaned (pointing to dead-ends or starting from dead-ends).
    # Delete those nodes such that there are no dead-ends.
    delete_dead_end_nodes(f_exploded, f_exploded_keep_n_id)


def get_connected_nodes_at_emission_idx(
        f_exploded: Graph[FORWARD_EXPLODED_NODE_ID, Any, FORWARD_EXPLODED_EDGE_ID, Any],
        f_exploded_keep_n_id: FORWARD_EXPLODED_NODE_ID
):
    f_exploded_keep_n_emission_idx, _ = f_exploded_keep_n_id
    pending = {f_exploded_keep_n_id}
    visited = set()
    while pending:
        f_exploded_n_id = pending.pop()
        visited.add(f_exploded_n_id)
        for _, _, f_exploded_to_n_id, _ in f_exploded.get_outputs_full(f_exploded_n_id):
            f_exploded_to_n_emission_idx, _ = f_exploded_to_n_id
            if f_exploded_keep_n_emission_idx == f_exploded_to_n_emission_idx and f_exploded_to_n_id not in visited:
                visited.add(f_exploded_to_n_id)
        for _, f_exploded_from_n_id, _, _ in f_exploded.get_inputs_full(f_exploded_n_id):
            f_exploded_from_n_emission_idx, _ = f_exploded_from_n_id
            if f_exploded_keep_n_emission_idx == f_exploded_from_n_emission_idx and f_exploded_from_n_id not in visited:
                visited.add(f_exploded_from_n_id)
    return visited


def delete_dead_end_nodes(
        f_exploded: Graph[FORWARD_EXPLODED_NODE_ID, Any, FORWARD_EXPLODED_EDGE_ID, Any],
        f_exploded_keep_n_id: FORWARD_EXPLODED_NODE_ID
):
    # Walk backwards to source
    pending = {f_exploded_keep_n_id}
    visited = set()
    while pending:
        f_exploded_n_id = pending.pop()
        visited.add(f_exploded_n_id)
        for _, f_exploded_from_n_id, _, _ in f_exploded.get_inputs_full(f_exploded_n_id):
            if f_exploded_from_n_id not in visited:
                pending.add(f_exploded_from_n_id)
    backward_visited = visited
    # Walk forward to sink
    pending = {f_exploded_keep_n_id}
    visited = set()
    while pending:
        f_exploded_n_id = pending.pop()
        visited.add(f_exploded_n_id)
        for _, _, f_exploded_to_n_id, _ in f_exploded.get_outputs_full(f_exploded_n_id):
            if f_exploded_to_n_id not in visited:
                pending.add(f_exploded_to_n_id)
    forward_visited = visited
    # Remove anything that wasn't touched (these are dead-ends)
    visited = backward_visited | forward_visited
    for f_exploded_n_id in set(f_exploded.get_nodes()):
        if f_exploded_n_id not in visited:
            f_exploded.delete_node(f_exploded_n_id)
```