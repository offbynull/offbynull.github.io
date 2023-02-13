`{bm-disable-all}`[ch10_code/src/profile_hmm/HMMSingleElementAlignment_InsertMatchDelete.py](ch10_code/src/profile_hmm/HMMSingleElementAlignment_InsertMatchDelete.py) (lines 13 to 70):`{bm-enable-all}`

```python
def create_hmm_square_from_v_perspective(
        transition_probabilities: dict[SEQ_HMM_STATE, dict[SEQ_HMM_STATE, float]],
        emission_probabilities: dict[SEQ_HMM_STATE, dict[SEQ_HMM_STATE, float]],
        hmm_top_left_n_id: SEQ_HMM_STATE,
        v_elem: tuple[int, ELEM | None],
        w_elem: tuple[int, ELEM | None],
        v_max_idx: int,
        w_max_idx: int,
        fake_bottom_right_emission_symbol: ELEM | None = None
):
    hmm_outgoing_n_ids = HMMSingleElementAlignment_EmitDelete.create_hmm_square_from_v_perspective(
        transition_probabilities,
        emission_probabilities,
        hmm_top_left_n_id,
        v_elem,
        w_elem,
        v_max_idx,
        w_max_idx,
        fake_bottom_right_emission_symbol
    )
    v_idx, v_symbol = v_elem
    w_idx, w_symbol = w_elem
    # Remove E10
    hmm_remove_n_id = 'E', v_idx + 1, w_idx
    if hmm_remove_n_id in transition_probabilities:
        removed_ep = emission_probabilities.pop(hmm_remove_n_id)
        removed_tp = transition_probabilities.pop(hmm_remove_n_id)
        if hmm_remove_n_id in hmm_outgoing_n_ids:
            hmm_outgoing_n_ids.remove(hmm_remove_n_id)
        # Replace with I10
        hmm_replace_match_n_id = 'I', v_idx + 1, w_idx
        transition_probabilities[hmm_replace_match_n_id] = removed_tp.copy()
        emission_probabilities[hmm_replace_match_n_id] = removed_ep.copy()
        transition_probabilities[hmm_top_left_n_id][hmm_replace_match_n_id] = transition_probabilities[hmm_top_left_n_id].pop(hmm_remove_n_id)
        hmm_outgoing_n_ids.add(hmm_replace_match_n_id)
    # Remove E11
    hmm_remove_n_id = 'E', v_idx + 1, w_idx + 1
    if hmm_remove_n_id in transition_probabilities:
        removed_ep = emission_probabilities.pop(hmm_remove_n_id)
        removed_tp = transition_probabilities.pop(hmm_remove_n_id)
        if hmm_remove_n_id in hmm_outgoing_n_ids:
            hmm_outgoing_n_ids.remove(hmm_remove_n_id)
        # Replace with M11
        hmm_replace_match_n_id = 'M', v_idx + 1, w_idx + 1
        transition_probabilities[hmm_replace_match_n_id] = removed_tp.copy()
        emission_probabilities[hmm_replace_match_n_id] = removed_ep.copy()
        transition_probabilities[hmm_top_left_n_id][hmm_replace_match_n_id] = transition_probabilities[hmm_top_left_n_id].pop(hmm_remove_n_id)
        hmm_outgoing_n_ids.add(hmm_replace_match_n_id)
        # Replace with I11
        hmm_bottom_left_n_id = 'D', v_idx, w_idx + 1
        hmm_replace_insert_n_id = 'I', v_idx + 1, w_idx + 1
        transition_probabilities[hmm_replace_insert_n_id] = removed_tp.copy()
        emission_probabilities[hmm_replace_insert_n_id] = removed_ep.copy()
        transition_probabilities[hmm_bottom_left_n_id][hmm_replace_insert_n_id] = transition_probabilities[hmm_bottom_left_n_id].pop(hmm_remove_n_id)
        hmm_outgoing_n_ids.add(hmm_replace_insert_n_id)
    # Return
    return hmm_outgoing_n_ids
```