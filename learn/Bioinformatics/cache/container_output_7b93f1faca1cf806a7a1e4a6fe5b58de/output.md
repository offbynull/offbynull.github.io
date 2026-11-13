`{bm-disable-all}`[ch10_code/src/profile_hmm/HMMProfileAlignment.py](ch10_code/src/profile_hmm/HMMProfileAlignment.py) (lines 85 to 155):`{bm-enable-all}`

```python
def hmm_profile_alignment(
        v_seq: list[ELEM],
        w_profile: Profile[ELEM],
        t_elem: ELEM,
        symbols: set[ELEM],
        pseudocount: float
):
    # Build graph
    transition_probabilities, emission_probabilities = create_profile_hmm_structure(v_seq, w_profile, t_elem)
    # Generate probabilities from profile
    emission_probabilities_overrides = profile_to_emission_probabilities(w_profile)
    transition_probability_overrides = profile_to_transition_probabilities(w_profile)
    # Apply generated transition probabilities
    for hmm_from_n_id in transition_probabilities:
        for hmm_to_n_id in transition_probabilities[hmm_from_n_id]:
            if hmm_to_n_id[0] == 'T':
                value = 1.0  # 100% chance of going to sink node
            else:
                _, _, row = hmm_from_n_id
                row -= 1
                direction, _, _ = hmm_to_n_id
                value = transition_probability_overrides[row][direction]
            transition_probabilities[hmm_from_n_id][hmm_to_n_id] = value
    # Apply generated emission probabilities
    for hmm_to_n_id in emission_probabilities:
        if hmm_to_n_id[0] == 'S':
            ...  # skip source, it's non-emitting
        elif hmm_to_n_id[0] == 'T':
            ...  # skip sink node, should have a single emission set to t_elem, which should already be in place
        elif hmm_to_n_id[0] == 'D':
            ...  # skip D nodes (deletions) as they are silent states (no emissions should happen)
        elif hmm_to_n_id[0] in {'I', 'M'}:
            direction, _, row = hmm_to_n_id
            row -= 1
            emit_probs = {sym: 0.0 for sym in symbols}
            emit_probs.update(emission_probabilities_overrides[row, direction])
            emission_probabilities[hmm_to_n_id] = emit_probs
        else:
            raise ValueError('Unknown node type -- this should never happen')
    # Build and apply pseudocounts
    transition_probabilities, emission_probabilities = stringify_probability_keys(transition_probabilities,
                                                                                  emission_probabilities)
    hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probabilities, emission_probabilities)
    hmm_add_pseudocounts_to_hidden_state_transition_probabilities(
        hmm,
        pseudocount
    )
    hmm_add_pseudocounts_to_symbol_emission_probabilities(
        hmm,
        pseudocount
    )
    # Get most probable hidden path (viterbi algorithm)
    hmm_source_n_id = hmm.get_root_node()
    hmm_sink_n_id = 'VITERBI_SINK'  # Fake sink node ID required for exploding HMM into Viterbi graph
    v_seq = v_seq + [t_elem]  # Add fake symbol for when exploding out Viterbi graph
    viterbi = to_viterbi_graph(hmm, hmm_source_n_id, hmm_sink_n_id, v_seq)
    probability, hidden_path = max_product_path_in_viterbi(viterbi)
    v_alignment = []
    # When looping, ignore phony end emission and Viterbi sink node at end: [(T, #, #), VITERBI_SINK].
    for hmm_from_n_id, hmm_to_n_id in hidden_path[:-2]:
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