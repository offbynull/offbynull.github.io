`{bm-disable-all}`[ch10_code/src/hmm/SymbolEmissionChainProbability.py](ch10_code/src/hmm/SymbolEmissionChainProbability.py) (lines 119 to 127):`{bm-enable-all}`

```python
def symbol_emission_chain_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        state_symbol_pairs: list[tuple[STATE, SYMBOL]],
) -> float:
    weight = 1.0
    for state, symbol in state_symbol_pairs:
        weight *= hmm.get_node_data(state).get_symbol_emission_probability(symbol)
    return weight
```