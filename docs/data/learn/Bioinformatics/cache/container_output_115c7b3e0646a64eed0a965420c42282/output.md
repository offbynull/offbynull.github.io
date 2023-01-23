`{bm-disable-all}`[ch10_code/src/hmm/EmpiricalLearning.py](ch10_code/src/hmm/EmpiricalLearning.py) (lines 131 to 154):`{bm-enable-all}`

```python
def derive_emission_probabilities(
        hmm: Graph[N, ND, E, ED],
        list_states: [[Graph[N, ND, E, ED]], Iterable[STATE]],
        list_symbols: [[Graph[N, ND, E, ED]], Iterable[SYMBOL]],
        get_node_emittable: Callable[[Graph[N, ND, E, ED], STATE], bool],
        observed_emissions: list[tuple[STATE, SYMBOL | None]]
) -> dict[tuple[STATE, SYMBOL], float]:
    dst_emission_counts = defaultdict(lambda: 0)
    dst_total_emission_counts = defaultdict(lambda: 0)
    for dst, symbol in observed_emissions:
        dst_emission_counts[dst, symbol] += 1
        dst_total_emission_counts[dst] += 1
    emission_probabilities = {}
    for dst in list_states(hmm):  # Query HMM for states (observed_emissions might miss some)
        if not get_node_emittable(hmm, dst):
            continue
        for symbol in list_symbols(hmm):
            if dst_total_emission_counts[dst] > 0:
                prob = dst_emission_counts[dst, symbol] / dst_total_emission_counts[dst]
            else:
                prob = 0.0
            emission_probabilities[dst, symbol] = prob
    return emission_probabilities
```