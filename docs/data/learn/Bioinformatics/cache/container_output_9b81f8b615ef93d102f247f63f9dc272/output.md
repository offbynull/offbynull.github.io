`{bm-disable-all}`[ch10_code/src/profile_hmm/ProfileToHMMProbabilities.py](ch10_code/src/profile_hmm/ProfileToHMMProbabilities.py) (lines 146 to 161):`{bm-enable-all}`

```python
def profile_to_transition_probabilities(profile: Profile[ELEM]):
    stable_row_cnt = profile.row_count
    # Count edges by groups
    counts = defaultdict(lambda: Counter())
    for profile_row in range(stable_row_cnt):
        walk = walk_row_of_profile(profile, profile_row)
        for (from_r, _), _, type, _ in walk:
            counts[from_r][type] += 1
    # Sum up counts for each column and divide to get probabilities
    percs = {}
    for from_r, from_counts in counts.items():
        percs[from_r] = {'I': 0.0, 'M': 0.0, 'D': 0.0}
        total = sum(from_counts.values())
        for k, v in from_counts.items():
            percs[from_r][k] = v / total
    return percs
```