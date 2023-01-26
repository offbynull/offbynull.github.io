`{bm-disable-all}`[ch10_code/src/hmm/StateTransitionFollowedBySymbolEmissionChainProbability.py](ch10_code/src/hmm/StateTransitionFollowedBySymbolEmissionChainProbability.py) (lines 119 to 129):`{bm-enable-all}`

```python
def state_transition_followed_by_symbol_emission_chain_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        transition_to_symbol_pairs: list[tuple[tuple[STATE, STATE], SYMBOL]],
) -> float:
    weight = 1.0
    for transition, to_symbol in transition_to_symbol_pairs:
        from_state, to_state = transition
        weight *= hmm.get_edge_data(transition).get_transition_probability() \
                  * hmm.get_node_data(to_state).get_symbol_emission_probability(to_symbol)
    return weight
```