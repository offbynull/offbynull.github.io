`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardBackwardSplitGraph.py](ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughNode_ForwardBackwardSplitGraph.py) (lines 17 to 111):`{bm-enable-all}`

```python
BACKWARD_EXPLODED_NODE_ID = tuple[FORWARD_EXPLODED_NODE_ID, int]
BACKWARD_EXPLODED_EDGE_ID = tuple[BACKWARD_EXPLODED_NODE_ID, BACKWARD_EXPLODED_NODE_ID]


def backward_explode(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        f_exploded: Graph[FORWARD_EXPLODED_NODE_ID, Any, FORWARD_EXPLODED_EDGE_ID, Any]
):
    f_exploded_source_n_id = f_exploded.get_root_node()
    f_exploded_sink_n_id = f_exploded.get_leaf_node()
    # Copy forward graph in the style of the backward graph
    b_exploded = Graph()
    for f_exploded_id in f_exploded.get_nodes():
        b_exploded_n_id = f_exploded_id, 0
        b_exploded.insert_node(b_exploded_n_id)
    for f_exploded_transition in f_exploded.get_edges():
        f_exploded_from_n_id, f_exploded_to_n_id = f_exploded_transition
        b_exploded_from_n_id = f_exploded_from_n_id, 0
        b_exploded_to_n_id = f_exploded_to_n_id, 0
        b_exploded_transition = b_exploded_from_n_id, b_exploded_to_n_id
        b_exploded.insert_edge(
            b_exploded_transition,
            b_exploded_from_n_id,
            b_exploded_to_n_id
        )
    # Duplicate nodes in backward graph based on transitions to non-emitting states
    b_exploded_n_counter = Counter()
    b_exploded_source_n_id = f_exploded_source_n_id, 0
    ready_set = {b_exploded_source_n_id}
    waiting_set = {}
    while ready_set:
        b_exploded_from_n_id = ready_set.pop()
        b_exploded_duplicated_from_n_ids = backward_exploded_duplicate_outwards(
            hmm,
            f_exploded_source_n_id,
            f_exploded_sink_n_id,
            b_exploded_from_n_id,
            b_exploded,
            b_exploded_n_counter
        )
        ready_set |= b_exploded_duplicated_from_n_ids
        for _, _, b_exploded_to_n_id, _ in b_exploded.get_outputs_full(b_exploded_from_n_id):
            if b_exploded_to_n_id not in waiting_set:
                waiting_set[b_exploded_to_n_id] = b_exploded.get_in_degree(b_exploded_to_n_id)
            waiting_set[b_exploded_to_n_id] -= 1
            if waiting_set[b_exploded_to_n_id] == 0:
                del waiting_set[b_exploded_to_n_id]
                ready_set.add(b_exploded_to_n_id)
    return b_exploded, b_exploded_n_counter


def backward_exploded_duplicate_outwards(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        f_exploded_source_n_id: FORWARD_EXPLODED_NODE_ID,
        f_exploded_sink_n_id: FORWARD_EXPLODED_NODE_ID,
        b_exploded_n_id: BACKWARD_EXPLODED_NODE_ID,
        b_exploded: Graph[BACKWARD_EXPLODED_NODE_ID, Any, BACKWARD_EXPLODED_EDGE_ID, Any],
        b_exploded_n_counter: Counter[FORWARD_EXPLODED_NODE_ID]
):
    # We're splitting based on outgoing edges -- if there's only a single outgoing edge, there's no point in trying to
    # split anything
    if b_exploded.get_out_degree(b_exploded_n_id) == 1:
        return set()
    f_exploded_n_id, _ = b_exploded_n_id
    # Source node shouldn't get duplicated
    if f_exploded_n_id == f_exploded_source_n_id:
        return set()
    b_exploded_new_n_ids = set()
    for _, _, b_exploded_to_n_id, _ in set(b_exploded.get_outputs_full(b_exploded_n_id)):
        f_exploded_to_n_id, _, = b_exploded_to_n_id
        _, hmm_to_n_id = f_exploded_to_n_id
        if f_exploded_to_n_id != f_exploded_sink_n_id and not hmm.get_node_data(hmm_to_n_id).is_emittable():
            b_exploded_n_counter[f_exploded_n_id] += 1
            b_exploded_new_n_count = b_exploded_n_counter[f_exploded_n_id]
            b_exploded_new_n_id = f_exploded_n_id, b_exploded_new_n_count
            b_exploded.insert_node(b_exploded_new_n_id)
            b_old_transition = b_exploded_n_id, b_exploded_to_n_id
            b_exploded.delete_edge(b_old_transition)
            b_new_transition = b_exploded_new_n_id, b_exploded_to_n_id
            b_exploded.insert_edge(
                b_new_transition,
                b_exploded_new_n_id,
                b_exploded_to_n_id
            )
            b_exploded_new_n_ids.add(b_exploded_new_n_id)
    for _, b_exploded_from_n_id, _, _ in b_exploded.get_inputs_full(b_exploded_n_id):
        for b_exploded_new_n_id in b_exploded_new_n_ids:
            b_new_transition = b_exploded_from_n_id, b_exploded_new_n_id
            b_exploded.insert_edge(
                b_new_transition,
                b_exploded_from_n_id,
                b_exploded_new_n_id
            )
    return b_exploded_new_n_ids
```