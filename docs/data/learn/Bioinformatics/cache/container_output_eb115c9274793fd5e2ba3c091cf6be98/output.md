`{bm-disable-all}`[ch10_code/src/profile_hmm/HMMSequenceAlignment.py](ch10_code/src/profile_hmm/HMMSequenceAlignment.py) (lines 146 to 207):`{bm-enable-all}`

```python
# Transition probabilities set to nan (they should be defined at some point later on).
# Emission probabilities set such that v has a 100% probability of emitting.
def create_hmm_square_from_w_perspective(
        transition_probabilities: dict[SEQ_HMM_STATE, dict[SEQ_HMM_STATE, float]],
        emission_probabilities: dict[SEQ_HMM_STATE, dict[SEQ_HMM_STATE, float]],
        hmm_top_left_n_id: SEQ_HMM_STATE,
        v_elem: tuple[int, ELEM | None],
        w_elem: tuple[int, ELEM | None],
        v_max_idx: int,
        w_max_idx: int
):
    v_idx, v_symbol = v_elem
    w_idx, w_symbol = w_elem
    hmm_outgoing_n_ids = set()
    # Make sure top-left exists
    if hmm_top_left_n_id not in transition_probabilities:
        transition_probabilities[hmm_top_left_n_id] = {}
        emission_probabilities[hmm_top_left_n_id] = {}
    # From top-left, go right (gap)
    if v_idx < v_max_idx:
        hmm_to_n_id = 'D', v_idx + 1, w_idx
        if hmm_to_n_id not in transition_probabilities:
            transition_probabilities[hmm_to_n_id] = {}
            emission_probabilities[hmm_to_n_id] = {}
        transition_probabilities[hmm_top_left_n_id][hmm_to_n_id] = nan
        hmm_outgoing_n_ids.add(hmm_to_n_id)
        # From top-left, after going right (gap), go downward (emit)
        if w_idx < w_max_idx:
            hmm_from_n_id = hmm_to_n_id
            hmm_to_n_id = 'E', v_idx + 1, w_idx + 1
            if hmm_to_n_id not in transition_probabilities:
                transition_probabilities[hmm_to_n_id] = {}
                emission_probabilities[hmm_to_n_id] = {}
            transition_probabilities[hmm_from_n_id][hmm_to_n_id] = nan
            emission_probabilities[hmm_to_n_id][w_symbol] = 1.0
            hmm_outgoing_n_ids.add(hmm_to_n_id)
    # From top-left, go downward (emit)
    if w_idx < w_max_idx:
        hmm_to_n_id = 'E', v_idx, w_idx + 1
        if hmm_to_n_id not in transition_probabilities:
            transition_probabilities[hmm_to_n_id] = {}
            emission_probabilities[hmm_to_n_id] = {}
        transition_probabilities[hmm_top_left_n_id][hmm_to_n_id] = nan
        emission_probabilities[hmm_to_n_id][w_symbol] = 1.0
        hmm_outgoing_n_ids.add(hmm_to_n_id)
        # From top-left, after going downward (emit), go right (gap)
        if v_idx < v_max_idx:
            hmm_from_n_id = hmm_to_n_id
            hmm_to_n_id = 'D', v_idx + 1, w_idx + 1
            if hmm_to_n_id not in transition_probabilities:
                transition_probabilities[hmm_to_n_id] = {}
                emission_probabilities[hmm_to_n_id] = {}
            transition_probabilities[hmm_from_n_id][hmm_to_n_id] = nan
    # From top-left, go diagonal (emit)
    if v_idx < v_max_idx and w_idx < w_max_idx:
        hmm_to_n_id = 'E', v_idx + 1, w_idx + 1
        transition_probabilities[hmm_top_left_n_id][hmm_to_n_id] = nan
        emission_probabilities[hmm_to_n_id][w_symbol] = 1.0
        hmm_outgoing_n_ids.add(hmm_to_n_id)
    # Return
    return hmm_outgoing_n_ids
```