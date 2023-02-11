`{bm-disable-all}`[ch10_code/src/profile_hmm/HMMSequenceAlignment.py](ch10_code/src/profile_hmm/HMMSequenceAlignment.py) (lines 264 to 304):`{bm-enable-all}`

```python
def create_hmm_chain_from_v_perspective(
        v_seq: list[ELEM],
        w_seq: list[ELEM]
):
    transition_probabilities = {}
    emission_probabilities = {}
    pending = set()
    processed = set()
    hmm_source_n_id = 'S', -1, -1
    hmm_outgoing_n_ids = create_hmm_square_from_v_perspective(
        transition_probabilities,
        emission_probabilities,
        hmm_source_n_id,
        (0, v_seq[0]),
        (0, w_seq[0]),
        len(v_seq),
        len(w_seq)
    )
    processed.add(hmm_source_n_id)
    pending |= hmm_outgoing_n_ids
    while pending:
        hmm_n_id = pending.pop()
        processed.add(hmm_n_id)
        _, v_idx, w_idx = hmm_n_id
        if v_idx <= len(v_seq) and w_idx <= len(w_seq):
            v_elem = None if v_idx == len(v_seq) else v_seq[v_idx]
            w_elem = None if w_idx == len(w_seq) else w_seq[w_idx]
            hmm_outgoing_n_ids = create_hmm_square_from_v_perspective(
                transition_probabilities,
                emission_probabilities,
                hmm_n_id,
                (v_idx, v_elem),
                (w_idx, w_elem),
                len(v_seq),
                len(w_seq)
            )
            for hmm_test_n_id in hmm_outgoing_n_ids:
                if hmm_test_n_id not in processed:
                    pending.add(hmm_test_n_id)
    return transition_probabilities, emission_probabilities
```