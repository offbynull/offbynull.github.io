`{bm-disable-all}`[ch10_code/src/hmm/MostProbableEmittedSequence_ForwardGraph.py](ch10_code/src/hmm/MostProbableEmittedSequence_ForwardGraph.py) (lines 207 to 269):`{bm-enable-all}`

```python
def compute_layer_exploded_max_emission_weights(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        f_exploded: Graph[LAYERED_FORWARD_EXPLODED_NODE_ID, Any, LAYERED_FORWARD_EXPLODED_EDGE_ID, float]
) -> float:
    # Use graph algorithm to figure out emission probability
    f_exploded_source_n_id = f_exploded.get_root_node()
    f_exploded_sink_n_id = f_exploded.get_leaf_node()
    f_exploded.update_node_data(f_exploded_source_n_id, (None, 1.0))
    f_exploded_to_n_ids = set()
    add_ready_to_process_outgoing_nodes(f_exploded, f_exploded_source_n_id, f_exploded_to_n_ids)
    while f_exploded_to_n_ids:
        f_exploded_to_n_id = f_exploded_to_n_ids.pop()
        f_exploded_to_n_emissions_idx, hmm_to_n_id, f_exploded_to_symbol = f_exploded_to_n_id
        # Determine symbol emission prob. In certain cases, the SINK node may exist in the HMM. Here we check that the
        # node exists in the HMM and that it's emmitable before getting the emission prob.
        if hmm.has_node(hmm_to_n_id) and hmm.get_node_data(hmm_to_n_id).is_emittable():
            symbol_emission_prob = hmm.get_node_data(hmm_to_n_id).get_symbol_emission_probability(f_exploded_to_symbol)
        else:
            symbol_emission_prob = 1.0  # No emission - setting to 1.0 means it has no effect in multiplication later on
        # Calculate forward weight for current node
        f_exploded_to_forward_weights = defaultdict(lambda: 0.0)
        for _, f_exploded_from_n_id, _, _ in f_exploded.get_inputs_full(f_exploded_to_n_id):
            _, hmm_from_n_id, f_exploded_from_symbol = f_exploded_from_n_id
            _, exploded_from_forward_weight = f_exploded.get_node_data(f_exploded_from_n_id)
            # Determine transition prob. In certain cases, the SINK node may exist in the HMM. Here we check that the
            # transition exists in the HMM. If it does, we use the transition prob.
            transition = hmm_from_n_id, hmm_to_n_id
            if hmm.has_edge(transition):
                transition_prob = hmm.get_edge_data(transition).get_transition_probability()
            else:
                transition_prob = 1.0  # Setting to 1.0 means it always happens
            f_exploded_to_forward_weights[
                f_exploded_from_symbol] += exploded_from_forward_weight * transition_prob * symbol_emission_prob
            # NOTE: The Pevzner book's formulas did it slightly differently. It factors out multiplication of
            # symbol_emission_prob such that it's applied only once after the loop finishes
            # (e.g. a*b*5+c*d*5+e*f*5 = 5*(a*b+c*d+e*f)). I didn't factor out symbol_emission_prob because I wanted the
            # code to line-up with the diagrams I created for the algorithm documentation.
        max_layer_symbol, max_value_value = max(f_exploded_to_forward_weights.items(), key=lambda item: item[1])
        f_exploded.update_node_data(f_exploded_to_n_id, (max_layer_symbol, max_value_value))
        # Now that the forward weight's been calculated for this node, check its outgoing neighbours to see if they're
        # also ready and add them to the ready set if they are.
        add_ready_to_process_outgoing_nodes(f_exploded, f_exploded_to_n_id, f_exploded_to_n_ids)
    # SINK node's weight should be the emission probability
    _, f_exploded_sink_forward_weight = f_exploded.get_node_data(f_exploded_sink_n_id)
    return f_exploded_sink_forward_weight


# Given a node in the exploded graph (exploded_n_from_id), look at each outgoing neighbours that it has
# (exploded_to_n_id). If that outgoing neighbour (exploded_to_n_id) has a "forward weight" set for all of its incoming
# neighbours, add it to the set of "ready_to_process" nodes.
def add_ready_to_process_outgoing_nodes(
        f_exploded: Graph[LAYERED_FORWARD_EXPLODED_NODE_ID, Any, LAYERED_FORWARD_EXPLODED_EDGE_ID, float],
        f_exploded_n_from_id: LAYERED_FORWARD_EXPLODED_NODE_ID,
        ready_to_process_n_ids: set[LAYERED_FORWARD_EXPLODED_NODE_ID]
):
    for _, _, f_exploded_to_n_id, _ in f_exploded.get_outputs_full(f_exploded_n_from_id):
        ready_to_process = True
        for _, n, _, _ in f_exploded.get_inputs_full(f_exploded_to_n_id):
            if f_exploded.get_node_data(n) is None:
                ready_to_process = False
        if ready_to_process:
            ready_to_process_n_ids.add(f_exploded_to_n_id)
```