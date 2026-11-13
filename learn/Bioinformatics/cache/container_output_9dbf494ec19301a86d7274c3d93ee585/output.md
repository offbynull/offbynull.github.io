`{bm-disable-all}`[ch10_code/src/hmm/StateTransitionChainProbability.py](ch10_code/src/hmm/StateTransitionChainProbability.py) (lines 121 to 129):`{bm-enable-all}`

```python
def state_transition_chain_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        state_transition: list[tuple[STATE, STATE]]
) -> float:
    weight = 1.0
    for t in state_transition:
        weight *= hmm.get_edge_data(t).get_transition_probability()
    return weight
```