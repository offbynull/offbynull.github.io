`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequence_Graph.py](ch10_code/src/hmm/ProbabilityOfEmittedSequence_Graph.py) (lines 219 to 289):`{bm-enable-all}`

```python
def emission_probability(
        hmm: Graph[N, ND, E, ED],
        hmm_source_n_id: N,
        hmm_sink_n_id: N,
        emitted_seq: list[SYMBOL],
        get_node_emission_prob: Callable[[Graph[N, ND, E, ED], STATE, SYMBOL], float],
        get_node_emittable: Callable[[Graph[N, ND, E, ED], STATE], bool],
        get_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE], float]
):
    # Explode out the HMM based on emitted_seq (same structure as a Viterbi graph)
    exploded = explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq, get_node_emittable)
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
        if get_node_emittable(hmm, hmm_to_n_id):
            symbol_emission_prob = get_node_emission_prob(hmm, hmm_to_n_id, symbol)
        else:
            symbol_emission_prob = 1.0
        # Calculate forward weight for current node
        exploded_to_forward_weight = 0.0
        for _, exploded_from_n_id, _, _ in exploded.get_inputs_full(exploded_to_n_id):
            _, hmm_from_n_id = exploded_from_n_id
            exploded_from_forward_weight = exploded.get_node_data(exploded_from_n_id)
            transition_prob = get_edge_transition_prob(hmm, hmm_from_n_id, hmm_to_n_id)
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
    return exploded, exploded_sink_forward_weight


# Given a node in the exploded graph (exploded_n_from_id), look at each outgoing neighbours that it has
# (exploded_to_n_id). If that outgoing neighbour (exploded_to_n_id) has a "forward weight" set for all of its incoming
# neighbours, add it to the set of "ready_to_process" nodes.
def add_ready_to_process_outgoing_nodes(
        exploded: Graph[tuple[int, N], Any, tuple[N, N], Any],
        exploded_n_from_id: tuple[int, N],
        ready_to_process_n_ids: set[tuple[int, N]]
):
    for _, _, exploded_to_n_id, _ in exploded.get_outputs_full(exploded_n_from_id):
        ready_to_process = all(exploded.get_node_data(n) is not None for _, n, _, _ in exploded.get_inputs_full(exploded_to_n_id))
        if ready_to_process:
            ready_to_process_n_ids.add(exploded_to_n_id)
```