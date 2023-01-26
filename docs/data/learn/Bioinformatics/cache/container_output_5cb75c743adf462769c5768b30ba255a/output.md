`{bm-disable-all}`[ch10_code/src/hmm/MostProbableHiddenPath_ViterbiPseudocounts.py](ch10_code/src/hmm/MostProbableHiddenPath_ViterbiPseudocounts.py) (lines 218 to 250):`{bm-enable-all}`

```python
def hmm_add_pseudocounts_to_hidden_state_transition_probabilities(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        psuedocount: float
) -> None:
    for from_state in hmm.get_nodes():
        tweaked_transition_weights = {}
        total_transition_probs = 0.0
        for transition in hmm.get_outputs(from_state):
            _, to_state = transition
            prob = hmm.get_edge_data(transition).get_transition_probability() + psuedocount
            tweaked_transition_weights[to_state] = prob
            total_transition_probs += prob
        for to_state, prob in tweaked_transition_weights.items():
            transition = from_state, to_state
            normalized_transition_prob = prob / total_transition_probs
            hmm.get_edge_data(transition).set_transition_probability(normalized_transition_prob)


def hmm_add_pseudocounts_to_symbol_emission_probabilities(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        psuedocount: float
) -> None:
    for from_state in hmm.get_nodes():
        tweaked_emission_weights = {}
        total_emission_probs = 0.0
        for symbol, prob in hmm.get_node_data(from_state).list_symbol_emissions():
            prob += psuedocount
            tweaked_emission_weights[symbol] = prob
            total_emission_probs += prob
        for symbol, prob in tweaked_emission_weights.items():
            normalized_transition_prob = prob / total_emission_probs
            hmm.get_node_data(from_state).set_symbol_emission_probability(symbol, normalized_transition_prob)
```