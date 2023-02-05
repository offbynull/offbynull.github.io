`{bm-disable-all}`[ch10_code/src/hmm/ViterbiLearning.py](ch10_code/src/hmm/ViterbiLearning.py) (lines 16 to 105):`{bm-enable-all}`

```python
def randomize_hmm_probabilities(
    hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData]
):
    for state in hmm.get_nodes():
        transitions = list(hmm.get_outputs(state))
        samples = [random() for _ in transitions]
        samples_sum = sum(samples)
        probs = [s / samples_sum for s in samples]
        for transition, probability in zip(transitions, probs):
            hmm.get_edge_data(transition).set_transition_probability(probability)
    for state in hmm.get_nodes():
        emissions = [s for s, _ in hmm.get_node_data(state).list_symbol_emissions()]
        samples = [random() for _ in emissions]
        samples_sum = sum(samples)
        probs = [s / samples_sum for s in samples]
        for symbol, probability in zip(emissions, probs):
            hmm.get_node_data(state).set_symbol_emission_probability(symbol, probability)


def viterbi_learning(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        pseudocount: float,
        cycles: int
) -> Generator[
    tuple[
        Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        dict[tuple[STATE, STATE], float],
        dict[tuple[STATE, SYMBOL], float],
        list[tuple[STATE, STATE]]
    ],
    None,
    None
]:
    # Assume first transition always begins from the SOURCE hidden state -- add it as non-emitting hidden state
    while cycles > 0:
        # Find most probable hidden path
        viterbi = to_viterbi_graph(
            hmm,
            hmm_source_n_id,
            hmm_sink_n_id,
            emitted_seq
        )
        _, hidden_path = max_product_path_in_viterbi(viterbi)
        hidden_path = hidden_path[:-1]  # Remove SINK transition from the path -- shouldn't be in original HMM
        # Refine observation by shoving in new path defined by the Viterbi graph
        observed_transitions_and_emissions = []
        for (from_state, to_state), to_symbol in zip(hidden_path, emitted_seq):
            observed_transitions_and_emissions.append((from_state, to_state, to_symbol))
        # Derive probabilities
        transition_probs = derive_transition_probabilities(
            hmm,
            [(from_state, to_state) for from_state, to_state, to_symbol in observed_transitions_and_emissions]
        )
        emission_probs = derive_emission_probabilities(
            hmm,
            [(dst, symbol) for src, dst, symbol in observed_transitions_and_emissions]
        )
        # Apply probabilities
        for transition, prob in transition_probs.items():
            hmm.get_edge_data(transition).set_transition_probability(prob)
        for (to_state, to_symbol), prob in emission_probs.items():
            hmm.get_node_data(to_state).set_symbol_emission_probability(to_symbol, prob)
        # Apply pseudocounts to probabilities
        hmm_add_pseudocounts_to_hidden_state_transition_probabilities(
            hmm,
            pseudocount
        )
        hmm_add_pseudocounts_to_symbol_emission_probabilities(
            hmm,
            pseudocount
        )
        # Override source state transitions such that they have equal probability of transitioning out. Should this be
        # enabled? The emitted sequence only has one transition from source, meaning that the learning process is going
        # to max out that transition.
        # source_transition_prob = 1.0 / hmm.get_out_degree(hmm_source_n_id)
        # for transition in hmm.get_outputs(hmm_source_n_id):
        #     hmm.get_edge_data(transition).set_transition_probability(source_transition_prob)
        # Extract out revised probabilities
        for transition in hmm.get_edges():
            transition_probs[transition] = hmm.get_edge_data(transition).get_transition_probability()
        for to_state in hmm.get_nodes():
            for to_symbol, prob in hmm.get_node_data(to_state).list_symbol_emissions():
                emission_probs[to_state, to_symbol] = prob
        # Yield
        yield hmm, transition_probs, emission_probs, hidden_path
        cycles -= 1
```