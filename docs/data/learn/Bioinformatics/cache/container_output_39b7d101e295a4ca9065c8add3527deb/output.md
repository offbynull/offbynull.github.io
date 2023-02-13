`{bm-disable-all}`[ch10_code/src/profile_hmm/HMMSequenceAlignment.py](ch10_code/src/profile_hmm/HMMSequenceAlignment.py) (lines 105 to 148):`{bm-enable-all}`

```python
def hmm_most_probable_from_v_perspective(
        v_seq: list[ELEM],
        w_seq: list[ELEM],
        transition_probability_overrides: dict[str, dict[str, float]],
        pseudocount: float
):
    transition_probabilities, emission_probabilities = create_hmm_chain_from_v_perspective(v_seq, w_seq)
    transition_probabilities, emission_probabilities = stringify_probability_keys(transition_probabilities,
                                                                                  emission_probabilities)
    for hmm_from_n_id in transition_probabilities:
        for hmm_to_n_id in transition_probabilities[hmm_from_n_id]:
            value = 1.0
            if hmm_from_n_id in transition_probability_overrides and \
                    hmm_to_n_id in transition_probability_overrides[hmm_from_n_id]:
                value = transition_probability_overrides[hmm_from_n_id][hmm_to_n_id]
            transition_probabilities[hmm_from_n_id][hmm_to_n_id] = value
    hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probabilities, emission_probabilities)
    hmm_add_pseudocounts_to_hidden_state_transition_probabilities(
        hmm,
        pseudocount
    )
    hmm_add_pseudocounts_to_symbol_emission_probabilities(
        hmm,
        pseudocount
    )
    hmm_source_n_id = hmm.get_root_node()
    hmm_sink_n_id = 'VITERBI_SINK'  # Fake sink node ID required for exploding HMM into Viterbi graph
    viterbi = to_viterbi_graph(hmm, hmm_source_n_id, hmm_sink_n_id, v_seq)
    probability, hidden_path = max_product_path_in_viterbi(viterbi)
    hidden_path = hidden_path[:-1]  # Remove viterbi sink node from end of path: VITERBI_SINK
    hidden_path = hidden_path[:-1]  # Remove HMM sink node from end of path: T
    v_alignment = []
    for hmm_from_n_id, hmm_to_n_id in hidden_path:
        state_type, to_v_idx, to_w_idx = hmm_to_n_id.split(',')
        to_v_idx = int(to_v_idx)
        to_w_idx = int(to_w_idx)
        if state_type == 'D':
            v_alignment.append(None)
        elif state_type in {'M', 'I'}:
            v_alignment.append(v_seq[to_v_idx - 1])
        else:
            raise ValueError('Unrecognizable type')
    return hmm, viterbi, probability, hidden_path, v_alignment
```