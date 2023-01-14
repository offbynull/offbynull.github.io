`{bm-disable-all}`[ch10_code/src/hmm/SymbolEmissionChainProbability.py](ch10_code/src/hmm/SymbolEmissionChainProbability.py) (lines 18 to 27):`{bm-enable-all}`

```python
def symbol_emission_chain_probability(
        hmm: Graph[N, ND, E, ED],
        state_symbol_pairs: list[tuple[STATE, SYMBOL]],
        get_node_emission_prob: Callable[[Graph[N, ND, E, ED], STATE, SYMBOL], float]
) -> float:
    weight = 1.0
    for state, symbol in state_symbol_pairs:
        weight *= get_node_emission_prob(hmm, state, symbol)
    return weight
```