`{bm-disable-all}`[ch10_code/src/hmm/EmpiricalLearning.py](ch10_code/src/hmm/EmpiricalLearning.py) (lines 170 to 191):`{bm-enable-all}`

```python
def derive_emission_probabilities(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        observed_emissions: list[tuple[STATE, SYMBOL | None]]
) -> dict[tuple[STATE, SYMBOL], float]:
    dst_emission_counts = defaultdict(lambda: 0)
    dst_total_emission_counts = defaultdict(lambda: 0)
    for to_state, symbol in observed_emissions:
        dst_emission_counts[to_state, symbol] += 1
        dst_total_emission_counts[to_state] += 1
    emission_probabilities = {}
    all_possible_symbols = {symbol for _, symbol in observed_emissions if symbol is not None}
    for to_state in hmm.get_nodes():  # Query HMM for states (observed_emissions might miss some)
        if not hmm.get_node_data(to_state).is_emittable():
            continue
        for symbol in all_possible_symbols:
            if dst_total_emission_counts[to_state] > 0:
                prob = dst_emission_counts[to_state, symbol] / dst_total_emission_counts[to_state]
            else:
                prob = 0.0
            emission_probabilities[to_state, symbol] = prob
    return emission_probabilities
```