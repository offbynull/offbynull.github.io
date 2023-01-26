`{bm-disable-all}`[ch10_code/src/hmm/EmpiricalLearning.py](ch10_code/src/hmm/EmpiricalLearning.py) (lines 148 to 166):`{bm-enable-all}`

```python
def derive_transition_probabilities(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        observed_transitions: list[tuple[STATE, STATE]]
) -> dict[tuple[STATE, STATE], float]:
    transition_counts = defaultdict(lambda: 0)
    transition_source_counts = defaultdict(lambda: 0)
    for from_state, to_state in observed_transitions:
        transition_counts[from_state, to_state] += 1
        transition_source_counts[from_state] += 1
    transition_probabilities = {}
    for transition in hmm.get_edges():  # Query HMM for transitions (observed_transitions might miss some)
        from_state, to_state = transition
        if transition_source_counts[from_state] > 0:
            prob = transition_counts[from_state, to_state] / transition_source_counts[from_state]
        else:
            prob = 0.0
        transition_probabilities[from_state, to_state] = prob
    return transition_probabilities
```