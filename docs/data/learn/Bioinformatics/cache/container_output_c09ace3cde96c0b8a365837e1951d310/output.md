`{bm-disable-all}`[ch10_code/src/hmm/StateTransitionFollowedBySymbolEmissionChainProbability.py](ch10_code/src/hmm/StateTransitionFollowedBySymbolEmissionChainProbability.py) (lines 17 to 27):`{bm-enable-all}`

```python
def state_transition_followed_by_symbol_emission_chain_probability(
        hmm: Graph[N, ND, E, ED],
        transition_to_symbol_pairs: list[tuple[tuple[STATE, STATE], SYMBOL]],
        get_node_emission_prob: Callable[[Graph[N, ND, E, ED], STATE, SYMBOL], float],
        get_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE], float]
) -> float:
    weight = 1.0
    for (from_state, to_state), to_symbol in transition_to_symbol_pairs:
        weight *= get_edge_transition_prob(hmm, from_state, to_state) * get_node_emission_prob(hmm, to_state, to_symbol)
    return weight
```