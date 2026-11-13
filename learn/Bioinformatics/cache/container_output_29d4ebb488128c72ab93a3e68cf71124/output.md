`{bm-disable-all}`[ch10_code/src/profile_hmm/HMMProfileAlignment.py](ch10_code/src/profile_hmm/HMMProfileAlignment.py) (lines 16 to 26):`{bm-enable-all}`

```python
def create_profile_hmm_structure(
        v_seq: list[ELEM],
        w_profile: Profile[ELEM],
        t_elem: ELEM
):
    # Create fake w_seq based on profile, just to feed into function for it to create the structure. This won't set any
    # probabilities (what's being returned are collections filled with NaN values).
    w_seq = [v_seq[0] for x in range(w_profile.col_count)]
    transition_probabilities, emission_probabilities = create_hmm_chain_from_v_perspective(v_seq, w_seq, t_elem)
    return transition_probabilities, emission_probabilities
```