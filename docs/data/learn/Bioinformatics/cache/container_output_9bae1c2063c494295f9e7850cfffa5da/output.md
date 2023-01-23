`{bm-disable-all}`[ch10_code/src/hmm/EmpiricalLearning.py](ch10_code/src/hmm/EmpiricalLearning.py) (lines 109 to 127):`{bm-enable-all}`

```python
def derive_transition_probabilities(
        hmm: Graph[N, ND, E, ED],
        list_state_transitions: Callable[[Graph[N, ND, E, ED]], Iterable[tuple[STATE, STATE]]],
        observed_transitions: list[tuple[STATE, STATE]]
) -> dict[tuple[STATE, STATE], float]:
    transition_counts = defaultdict(lambda: 0)
    transition_source_counts = defaultdict(lambda: 0)
    for src, dst in observed_transitions:
        transition_counts[src, dst] += 1
        transition_source_counts[src] += 1
    transition_probabilities = {}
    for src, dst in list_state_transitions(hmm):  # Query HMM for transitions (observed_transitions might miss some)
        if transition_source_counts[src] > 0:
            prob = transition_counts[src, dst] / transition_source_counts[src]
        else:
            prob = 0.0
        transition_probabilities[src, dst] = prob
    return transition_probabilities
```