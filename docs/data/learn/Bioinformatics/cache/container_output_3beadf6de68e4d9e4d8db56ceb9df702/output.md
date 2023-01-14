`{bm-disable-all}`[ch10_code/src/hmm/StateTransitionChainProbability.py](ch10_code/src/hmm/StateTransitionChainProbability.py) (lines 17 to 26):`{bm-enable-all}`

```python
def state_transition_chain_probability(
        hmm: Graph[N, ND, E, ED],
        states: list[tuple[STATE, STATE]],
        get_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE], float]
) -> float:
    weight = 1.0
    for from_state, to_state in states:
        weight *= get_edge_transition_prob(hmm, from_state, to_state)
    return weight
```