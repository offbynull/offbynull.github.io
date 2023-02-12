`{bm-disable-all}`[ch10_code/src/profile_hmm/HMMSingleElementAlignment_EmitDelete.py](ch10_code/src/profile_hmm/HMMSingleElementAlignment_EmitDelete.py) (lines 34 to 116):`{bm-enable-all}`

```python
SEQ_HMM_STATE = tuple[str, int, int]


# Transition probabilities set to nan (they should be defined at some point later on).
# Emission probabilities set such that v has a 100% probability of emitting.
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
        hmm_to_n_id = 'E', v_idx + 1, w_idx
        if hmm_to_n_id not in transition_probabilities:
            transition_probabilities[hmm_to_n_id] = {}
            emission_probabilities[hmm_to_n_id] = {}
        transition_probabilities[hmm_top_left_n_id][hmm_to_n_id] = nan
        emission_probabilities[hmm_to_n_id][v_symbol] = 1.0
        hmm_outgoing_n_ids.add(hmm_to_n_id)
        # From top-left, after going right (emit), go downward (gap)
        if w_idx < w_max_idx:
            hmm_from_n_id = hmm_to_n_id
            hmm_to_n_id = 'D', v_idx + 1, w_idx + 1
            if hmm_to_n_id not in transition_probabilities:
                transition_probabilities[hmm_to_n_id] = {}
                emission_probabilities[hmm_to_n_id] = {}
            transition_probabilities[hmm_from_n_id][hmm_to_n_id] = nan
            hmm_outgoing_n_ids.add(hmm_to_n_id)
    # From top-left, go downward (gap)
    if w_idx < w_max_idx:
        hmm_to_n_id = 'D', v_idx, w_idx + 1
        if hmm_to_n_id not in transition_probabilities:
            transition_probabilities[hmm_to_n_id] = {}
            emission_probabilities[hmm_to_n_id] = {}
        transition_probabilities[hmm_top_left_n_id][hmm_to_n_id] = nan
        hmm_outgoing_n_ids.add(hmm_to_n_id)
        # From top-left, after going downward (gap), go right (emit)
        if v_idx < v_max_idx:
            hmm_from_n_id = hmm_to_n_id
            hmm_to_n_id = 'E', v_idx + 1, w_idx + 1
            if hmm_to_n_id not in transition_probabilities:
                transition_probabilities[hmm_to_n_id] = {}
                emission_probabilities[hmm_to_n_id] = {}
            transition_probabilities[hmm_from_n_id][hmm_to_n_id] = nan
            emission_probabilities[hmm_to_n_id][v_symbol] = 1.0
            hmm_outgoing_n_ids.add(hmm_to_n_id)
    # From top-left, go diagonal (emit)
    if v_idx < v_max_idx and w_idx < w_max_idx:
        hmm_to_n_id = 'E', v_idx + 1, w_idx + 1
        transition_probabilities[hmm_top_left_n_id][hmm_to_n_id] = nan
        emission_probabilities[hmm_to_n_id][v_symbol] = 1.0
        hmm_outgoing_n_ids.add(hmm_to_n_id)
    # Add fake bottom-right emission (if it's been asked for)
    if fake_bottom_right_emission_symbol is not None:
        hmm_bottom_right_n_id_final = 'T', v_idx + 1, w_idx + 1
        hmm_bottom_right_n_id_1 = 'E', v_idx + 1, w_idx + 1
        if hmm_bottom_right_n_id_1 in hmm_outgoing_n_ids:
            transition_probabilities[hmm_bottom_right_n_id_1][hmm_bottom_right_n_id_final] = nan
            transition_probabilities[hmm_bottom_right_n_id_final] = {}
            emission_probabilities[hmm_bottom_right_n_id_final] = {fake_bottom_right_emission_symbol: 1.0}
            hmm_outgoing_n_ids.remove(hmm_bottom_right_n_id_1)
        hmm_bottom_right_n_id_2 = 'D', v_idx + 1, w_idx + 1
        if hmm_bottom_right_n_id_2 in hmm_outgoing_n_ids:
            transition_probabilities[hmm_bottom_right_n_id_2][hmm_bottom_right_n_id_final] = nan
            transition_probabilities[hmm_bottom_right_n_id_final] = {}
            emission_probabilities[hmm_bottom_right_n_id_final] = {fake_bottom_right_emission_symbol: 1.0}
            hmm_outgoing_n_ids.remove(hmm_bottom_right_n_id_2)
        hmm_outgoing_n_ids.add(hmm_bottom_right_n_id_final)
    # Return
    return hmm_outgoing_n_ids
```