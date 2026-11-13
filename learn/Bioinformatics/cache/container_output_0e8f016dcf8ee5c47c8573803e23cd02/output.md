`{bm-disable-all}`[ch10_code/src/hmm/BaumWelchLearning.py](ch10_code/src/hmm/BaumWelchLearning.py) (lines 61 to 84):`{bm-enable-all}`

```python
def node_certainties_to_emission_probabilities(hmm, hmm_sink_n_id, hmm_source_n_id, emitted_seq):
    _, _, f_exploded_n_certainties = node_certainties(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    # Sum up emission certainties. Everytime the hidden state N emits C, its certainty gets added to ...
    #  * summed_emission_certainties[N, C]           - groups by (N,C) and sums each group
    #  * summed_emission_certainties_by_to_state[N]  - groups by N and sums each group
    summed_emission_certainties = defaultdict(lambda: 0.0)
    summed_emission_certainties_by_to_state = defaultdict(lambda: 0.0)
    for f_exploded_to_n_id, certainty in f_exploded_n_certainties.items():
        f_exploded_to_n_emission_idx, hmm_to_n_id = f_exploded_to_n_id
        # if hmm_to_n_id == hmm_source_n_id or hmm_to_n_id == hmm_sink_n_id:
        #     continue
        symbol = emitted_seq[f_exploded_to_n_emission_idx]
        summed_emission_certainties[hmm_to_n_id, symbol] += certainty
        summed_emission_certainties_by_to_state[hmm_to_n_id] += certainty
    # Calculate new emission probabilities:
    # For each emission in the HMM (N,C), set that emission's probability using the certainty sums.
    # Specifically, the sum of certainties for (N,C) divided by the sum of all certainties from N.
    emission_probs = defaultdict(lambda: 0.0)
    for hmm_to_n_id, symbol in summed_emission_certainties:
        portion = summed_emission_certainties[hmm_to_n_id, symbol]
        total = summed_emission_certainties_by_to_state[hmm_to_n_id]
        emission_probs[hmm_to_n_id, symbol] = portion / total
    return emission_probs
```