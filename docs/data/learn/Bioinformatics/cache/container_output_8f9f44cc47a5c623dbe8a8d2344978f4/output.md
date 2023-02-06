`{bm-disable-all}`[ch10_code/src/hmm/BaumWelchLearning.py](ch10_code/src/hmm/BaumWelchLearning.py) (lines 88 to 113):`{bm-enable-all}`

```python
def edge_certainties_to_transition_probabilities(hmm, hmm_sink_n_id, hmm_source_n_id, emitted_seq):
    _, _, f_exploded_e_certainties = edge_certainties(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    # Sum up transition certainties. Everytime the transition S->E is encountered, its certainty gets added to ...
    #  * summed_transition_certainties[S, E]             - groups by (S,E) and sums each group
    #  * summed_transition_certainties_by_from_state[S]  - groups by S and sums each group
    summed_transition_certainties = defaultdict(lambda: 0.0)
    summed_transition_certainties_by_from_state = defaultdict(lambda: 0.0)
    for (f_exploded_from_n_id, f_exploded_to_n_id), certainty in f_exploded_e_certainties.items():
        _, hmm_from_n_id = f_exploded_from_n_id
        _, hmm_to_n_id = f_exploded_to_n_id
        # Sink node may not exist in the HMM. The check below tests for that and skips if it doesn't exist.
        transition = hmm_from_n_id, hmm_to_n_id
        if not hmm.has_edge(transition):
            continue
        summed_transition_certainties[hmm_from_n_id, hmm_to_n_id] += certainty
        summed_transition_certainties_by_from_state[hmm_from_n_id] += certainty
    # Calculate new transition probabilities:
    # For each transition in the HMM (S,E), set that transition's probability using the certainty sums.
    # Specifically, the sum of certainties for (S,E) divided by the sum of all certainties starting from S.
    transition_probs = defaultdict(lambda: 0.0)
    for hmm_from_n_id, hmm_to_n_id in summed_transition_certainties:
        portion = summed_transition_certainties[hmm_from_n_id, hmm_to_n_id]
        total = summed_transition_certainties_by_from_state[hmm_from_n_id]
        transition_probs[hmm_from_n_id, hmm_to_n_id] = portion / total
    return transition_probs
```