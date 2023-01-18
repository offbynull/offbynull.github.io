`{bm-disable-all}`[ch10_code/src/hmm/MostProbableHiddenPath_ViterbiPseudocounts.py](ch10_code/src/hmm/MostProbableHiddenPath_ViterbiPseudocounts.py) (lines 167 to 205):`{bm-enable-all}`

```python
def hmm_add_pseudocounts_to_hidden_state_transition_probabilities(
        hmm: Graph[N, ND, E, ED],
        psuedocount: float,
        list_states: [[Graph[N, ND, E, ED]], Iterable[STATE]],
        list_outgoing_state_transitions: [[Graph[N, ND, E, ED], STATE], Iterable[STATE]],
        get_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE], float],
        set_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE, float], None]
) -> None:
    for from_state in list_states(hmm):
        tweaked_transition_weights = {}
        total_transition_weights = 0.0
        for to_state in list_outgoing_state_transitions(hmm, from_state):
            weight = get_edge_transition_prob(hmm, from_state, to_state) + psuedocount
            tweaked_transition_weights[to_state] = weight
            total_transition_weights += weight
        for to_state, weight in tweaked_transition_weights.items():
            normalized_transition_weight = weight / total_transition_weights
            set_edge_transition_prob(hmm, from_state, to_state, normalized_transition_weight)


def hmm_add_pseudocounts_to_symbol_emission_probabilities(
        hmm: Graph[N, ND, E, ED],
        psuedocount: float,
        list_states: [[Graph[N, ND, E, ED]], Iterable[STATE]],
        list_state_emissions: [[Graph[N, ND, E, ED]], Iterable[SYMBOL]],
        get_node_emission_prob: Callable[[Graph[N, ND, E, ED], STATE, SYMBOL], float],
        set_node_emission_prob: Callable[[Graph[N, ND, E, ED], STATE, SYMBOL, float], None],
) -> None:
    for from_state in list_states(hmm):
        tweaked_emission_weights = {}
        total_emission_weights = 0.0
        for symbol in list_state_emissions(hmm, from_state):
            weight = get_node_emission_prob(hmm, from_state, symbol) + psuedocount
            tweaked_emission_weights[symbol] = weight
            total_emission_weights += weight
        for symbol, weight in tweaked_emission_weights.items():
            normalized_transition_weight = weight / total_emission_weights
            set_node_emission_prob(hmm, from_state, symbol, normalized_transition_weight)
```