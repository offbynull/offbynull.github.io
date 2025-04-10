`{bm-disable-all}`[ch10_code/src/profile_hmm/HMMSingleElementAlignment_InsertMatchDelete.py](ch10_code/src/profile_hmm/HMMSingleElementAlignment_InsertMatchDelete.py) (lines 13 to 106):`{bm-enable-all}`

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
    v_idx, v_symbol = v_elem
    w_idx, w_symbol = w_elem
    hmm_outgoing_n_ids = set()
    # Make sure top-left exists
    if hmm_top_left_n_id not in transition_probabilities:
        transition_probabilities[hmm_top_left_n_id] = {}
        emission_probabilities[hmm_top_left_n_id] = {}
    # From top-left, go right (emit)
    if v_idx < v_max_idx:
        hmm_to_n_id = 'I', v_idx + 1, w_idx
        inject_emitable(
            transition_probabilities,
            emission_probabilities,
            hmm_top_left_n_id,
            hmm_to_n_id,
            v_symbol,
            hmm_outgoing_n_ids
        )
        # From top-left, after going right (emit), go downward (gap)
        if w_idx < w_max_idx:
            hmm_from_n_id = hmm_to_n_id
            hmm_to_n_id = 'D', v_idx + 1, w_idx + 1
            inject_non_emittable(
                transition_probabilities,
                emission_probabilities,
                hmm_from_n_id,
                hmm_to_n_id,
                hmm_outgoing_n_ids
            )
    # From top-left, go downward (gap)
    if w_idx < w_max_idx:
        hmm_to_n_id = 'D', v_idx, w_idx + 1
        inject_non_emittable(
            transition_probabilities,
            emission_probabilities,
            hmm_top_left_n_id,
            hmm_to_n_id,
            hmm_outgoing_n_ids
        )
        # From top-left, after going downward (gap), go right (emit)
        if v_idx < v_max_idx:
            hmm_from_n_id = hmm_to_n_id
            hmm_to_n_id = 'I', v_idx + 1, w_idx + 1
            inject_emitable(
                transition_probabilities,
                emission_probabilities,
                hmm_from_n_id,
                hmm_to_n_id,
                v_symbol,
                hmm_outgoing_n_ids
            )
    # From top-left, go diagonal (emit)
    if v_idx < v_max_idx and w_idx < w_max_idx:
        hmm_to_n_id = 'M', v_idx + 1, w_idx + 1
        inject_emitable(
            transition_probabilities,
            emission_probabilities,
            hmm_top_left_n_id,
            hmm_to_n_id,
            v_symbol,
            hmm_outgoing_n_ids
        )
    # Add fake bottom-right emission (if it's been asked for)
    if fake_bottom_right_emission_symbol is not None:
        hmm_bottom_right_n_id_final = 'T', v_idx + 1, w_idx + 1
        hmm_bottom_right_n_ids = {
            ('M', v_idx + 1, w_idx + 1),
            ('D', v_idx + 1, w_idx + 1),
            ('I', v_idx + 1, w_idx + 1)
        }
        for hmm_bottom_right_n_id in hmm_bottom_right_n_ids:
            if hmm_bottom_right_n_id in hmm_outgoing_n_ids:
                inject_emitable(
                    transition_probabilities,
                    emission_probabilities,
                    hmm_bottom_right_n_id,
                    hmm_bottom_right_n_id_final,
                    fake_bottom_right_emission_symbol,
                    hmm_outgoing_n_ids
                )
                hmm_outgoing_n_ids.remove(hmm_bottom_right_n_id)
    # Return
    return hmm_outgoing_n_ids
```