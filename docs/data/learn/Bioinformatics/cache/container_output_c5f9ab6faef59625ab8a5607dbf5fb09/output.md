`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequenceWithIndexEmittingFromHiddenState_Graph.py](ch10_code/src/hmm/ProbabilityOfEmittedSequenceWithIndexEmittingFromHiddenState_Graph.py) (lines 268 to 361):`{bm-enable-all}`

```python
def emission_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        emitted_seq_idx_of_interest: int,
        hidden_state_of_interest: STATE
):
    # Compute on full exploded HMM
    full_exploded = explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    full_probs_sum = exploded_hmm_calculation(hmm, full_exploded, emitted_seq)
    # Compute on isolated exploded HMM
    # NOTE: Instead of re-exploding the graph again, you can just use the same exploded HMM as above. I did it like this
    #       because I want the code to display both graphs. The other options to doing this were to use callbacks or
    #       yield statements, both of which make the function more complicated to understand.
    isolated_exploded = explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    for exploded_n_id in set(isolated_exploded.get_nodes()):
        emitted_seq_idx, hmm_n_id = exploded_n_id
        if emitted_seq_idx == emitted_seq_idx_of_interest and hmm_n_id != hidden_state_of_interest\
                and hmm.get_node_data(hmm_n_id).is_emittable():
            delete_exploded_n_id = emitted_seq_idx, hmm_n_id
            isolated_exploded.delete_node(delete_exploded_n_id)
    isolated_probs_sum = exploded_hmm_calculation(hmm, isolated_exploded, emitted_seq)
    # Determine certainty and return
    certainty = isolated_probs_sum / full_probs_sum
    return full_exploded, isolated_exploded, certainty


def exploded_hmm_calculation(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        exploded: Graph[EXPLODED_NODE_ID, Any, EXPLODED_EDGE_ID, Any],
        emitted_seq: list[SYMBOL]
) -> float:
    # Use graph algorithm to figure out emission probability
    exploded_source_n_id = exploded.get_root_node()  # equiv to (-1, hmm_source_n_id) -- using root node func for clarity
    exploded_sink_n_id = exploded.get_leaf_node()  # equiv to (-1, hmm_sink_n_id) -- using leaf node func for clarity
    exploded.update_node_data(exploded_source_n_id, 1.0)
    exploded_to_n_ids = set()
    add_ready_to_process_outgoing_nodes(exploded, exploded_source_n_id, exploded_to_n_ids)
    while exploded_to_n_ids:
        exploded_to_n_id = exploded_to_n_ids.pop()
        # Don't process SINK node in this loop because of the emittable check / emission probability extraction: The
        # sink node is not a hidden state in the HMM (it's only a node in the exploded graph) meaning it will fail if
        # you try to query if its emittable / its emission probabilities.
        if exploded_to_n_id == exploded_sink_n_id:
            continue
        exploded_to_n_emissions_idx, hmm_to_n_id = exploded_to_n_id
        # Get the symbol emission probability for some symbol at the current hidden state. If the hidden state is
        # non-emittable, use 1.0 instead.
        symbol = emitted_seq[exploded_to_n_emissions_idx]
        if hmm.get_node_data(hmm_to_n_id).is_emittable():
            symbol_emission_prob = hmm.get_node_data(hmm_to_n_id).get_symbol_emission_probability(symbol)
        else:
            symbol_emission_prob = 1.0
        # Calculate forward weight for current node
        exploded_to_forward_weight = 0.0
        for _, exploded_from_n_id, _, _ in exploded.get_inputs_full(exploded_to_n_id):
            _, hmm_from_n_id = exploded_from_n_id
            exploded_from_forward_weight = exploded.get_node_data(exploded_from_n_id)
            transition = hmm_from_n_id, hmm_to_n_id
            transition_prob = hmm.get_edge_data(transition).get_transition_probability()
            exploded_to_forward_weight += exploded_from_forward_weight * transition_prob * symbol_emission_prob
            # NOTE: The Pevzner book's formulas did it slightly differently. It factors out multiplication of
            # symbol_emission_prob such that it's applied only once after the loop finishes
            # (e.g. a*b*5+c*d*5+e*f*5 = 5*(a*b+c*d+e*f)). I didn't factor out symbol_emission_prob because I wanted the
            # code to line-up with the diagrams I created for the algorithm documentation.
        exploded.update_node_data(exploded_to_n_id, exploded_to_forward_weight)
        # Now that the forward weight's been calculated for this node, check its outgoing neighbours to see if they're
        # also ready and add them to the ready set if they are.
        add_ready_to_process_outgoing_nodes(exploded, exploded_to_n_id, exploded_to_n_ids)
    # The code above doesn't cover the SINK node -- run a cycle for the SINK node as well here.
    exploded_sink_forward_weight = 0.0
    for _, exploded_from_n_id, _, _ in exploded.get_inputs_full(exploded_sink_n_id):
        exploded_from_forward_weight = exploded.get_node_data(exploded_from_n_id)
        transition_prob = 1.0
        exploded_sink_forward_weight += exploded_from_forward_weight * transition_prob
    exploded.update_node_data(exploded_sink_n_id, exploded_sink_forward_weight)
    # SINK node's weight should be the emission probability
    return exploded_sink_forward_weight


# Given a node in the exploded graph (exploded_n_from_id), look at each outgoing neighbours that it has
# (exploded_to_n_id). If that outgoing neighbour (exploded_to_n_id) has a "forward weight" set for all of its incoming
# neighbours, add it to the set of "ready_to_process" nodes.
def add_ready_to_process_outgoing_nodes(
        exploded: Graph[EXPLODED_NODE_ID, Any, EXPLODED_EDGE_ID, Any],
        exploded_n_from_id: EXPLODED_NODE_ID,
        ready_to_process_n_ids: set[EXPLODED_NODE_ID]
):
    for _, _, exploded_to_n_id, _ in exploded.get_outputs_full(exploded_n_from_id):
        ready_to_process = all(exploded.get_node_data(n) is not None for _, n, _, _ in exploded.get_inputs_full(exploded_to_n_id))
        if ready_to_process:
            ready_to_process_n_ids.add(exploded_to_n_id)
```