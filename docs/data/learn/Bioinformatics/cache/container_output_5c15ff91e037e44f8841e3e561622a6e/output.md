`{bm-disable-all}`[ch10_code/src/hmm/MostProbableEmittedSequence_Graph.py](ch10_code/src/hmm/MostProbableEmittedSequence_Graph.py) (lines 341 to 424):`{bm-enable-all}`

```python
def compute_exploded_max_emission_weights(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        exploded: Graph[EXPLODED_NODE_ID, Any, EXPLODED_EDGE_ID, float]
) -> float:
    # Use graph algorithm to figure out emission probability
    exploded_source_n_id = exploded.get_root_node()  # equiv to (-1, hmm_source_n_id) -- using root node func for clarity
    exploded_sink_n_id = exploded.get_leaf_node()  # equiv to (-1, hmm_sink_n_id) -- using leaf node func for clarity
    exploded.update_node_data(exploded_source_n_id, (None, 1.0))
    exploded_to_n_ids = set()
    add_ready_to_process_outgoing_nodes(exploded, exploded_source_n_id, exploded_to_n_ids)
    while exploded_to_n_ids:
        exploded_to_n_id = exploded_to_n_ids.pop()
        # Don't process SINK node in this loop because of the emittable check / emission probability extraction: The
        # sink node is not a hidden state in the HMM (it's only a node in the exploded graph) meaning it will fail if
        # you try to query if its emittable / its emission probabilities.
        if exploded_to_n_id == exploded_sink_n_id:
            continue
        compute_node_forward_weight(hmm, exploded, exploded_to_n_id)
        # Now that the forward weight's been calculated for this node, check its outgoing neighbours to see if they're
        # also ready and add them to the ready set if they are.
        add_ready_to_process_outgoing_nodes(exploded, exploded_to_n_id, exploded_to_n_ids)
    # The code above doesn't cover the SINK node -- run a cycle for the SINK node as well here.
    compute_sink_node_forward_weight(exploded, exploded_sink_n_id)
    # SINK node's weight should be the emission probability
    _, exploded_sink_forward_weight = exploded.get_node_data(exploded_sink_n_id)
    return exploded_sink_forward_weight


def compute_node_forward_weight(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        exploded: Graph[EXPLODED_NODE_ID, Any, EXPLODED_EDGE_ID, float],
        exploded_to_n_id: EXPLODED_NODE_ID
):
    exploded_to_n_emissions_idx, hmm_to_n_id, exploded_to_symbol = exploded_to_n_id
    # Get the symbol emission probability for some symbol at the current hidden state. If the hidden state is
    # non-emittable, use 1.0 instead.
    if hmm.get_node_data(hmm_to_n_id).is_emittable():
        symbol_emission_prob = hmm.get_node_data(hmm_to_n_id).get_symbol_emission_probability(exploded_to_symbol)
    else:
        symbol_emission_prob = 1.0
    # Calculate forward weight for current node
    exploded_to_forward_weights = defaultdict(lambda: 0.0)
    for _, exploded_from_n_id, _, _ in exploded.get_inputs_full(exploded_to_n_id):
        _, hmm_from_n_id, exploded_from_symbol = exploded_from_n_id
        _, exploded_from_forward_weight = exploded.get_node_data(exploded_from_n_id)
        transition = hmm_from_n_id, hmm_to_n_id
        transition_prob = hmm.get_edge_data(transition).get_transition_probability()
        exploded_to_forward_weights[exploded_from_symbol] += exploded_from_forward_weight * transition_prob * symbol_emission_prob
        # NOTE: The Pevzner book's formulas did it slightly differently. It factors out multiplication of
        # symbol_emission_prob such that it's applied only once after the loop finishes
        # (e.g. a*b*5+c*d*5+e*f*5 = 5*(a*b+c*d+e*f)). I didn't factor out symbol_emission_prob because I wanted the
        # code to line-up with the diagrams I created for the algorithm documentation.
    max_layer_symbol, max_value_value = max(exploded_to_forward_weights.items(), key=lambda item: item[1])
    exploded.update_node_data(exploded_to_n_id, (max_layer_symbol, max_value_value))


def compute_sink_node_forward_weight(
        exploded: Graph[EXPLODED_NODE_ID, Any, EXPLODED_EDGE_ID, float],
        exploded_sink_n_id: EXPLODED_NODE_ID
):
    transition_prob = 1.0
    # Calculate forward weight for current node
    exploded_to_forward_weights = defaultdict(lambda: 0.0)
    for _, exploded_from_n_id, _, _ in exploded.get_inputs_full(exploded_sink_n_id):
        _, hmm_from_n_id, exploded_from_symbol = exploded_from_n_id
        _, exploded_from_forward_weight = exploded.get_node_data(exploded_from_n_id)
        exploded_to_forward_weights[exploded_from_symbol] += exploded_from_forward_weight * transition_prob
    max_layer_symbol, max_value_value = max(exploded_to_forward_weights.items(), key=lambda item: item[1])
    exploded.update_node_data(exploded_sink_n_id, (max_layer_symbol, max_value_value))


# Given a node in the exploded graph (exploded_n_from_id), look at each outgoing neighbours that it has
# (exploded_to_n_id). If that outgoing neighbour (exploded_to_n_id) has a "forward weight" set for all of its incoming
# neighbours, add it to the set of "ready_to_process" nodes.
def add_ready_to_process_outgoing_nodes(
        exploded: Graph[EXPLODED_NODE_ID, Any, EXPLODED_EDGE_ID, float],
        exploded_n_from_id: EXPLODED_NODE_ID,
        ready_to_process_n_ids: set[EXPLODED_NODE_ID]
):
    for _, _, exploded_to_n_id, _ in exploded.get_outputs_full(exploded_n_from_id):
        ready_to_process = all(exploded.get_node_data(n) is not None for _, n, _, _ in exploded.get_inputs_full(exploded_to_n_id))
        if ready_to_process:
            ready_to_process_n_ids.add(exploded_to_n_id)
```