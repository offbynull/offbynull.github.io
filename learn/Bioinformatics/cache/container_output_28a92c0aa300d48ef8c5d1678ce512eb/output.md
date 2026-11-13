`{bm-disable-all}`[ch10_code/src/profile_hmm/ProfileToHMMProbabilities.py](ch10_code/src/profile_hmm/ProfileToHMMProbabilities.py) (lines 85 to 101):`{bm-enable-all}`

```python
def profile_to_emission_probabilities(profile: Profile[ELEM]):
    stable_row_cnt = profile.row_count
    # Count edges by groups
    counts = defaultdict(lambda: Counter())
    for profile_row in range(stable_row_cnt):
        walk = walk_row_of_profile(profile, profile_row)
        for _, (to_r, _), type, elems in walk:
            for elem in elems:
                if elem is not None:
                    counts[to_r, type][elem] += 1
    # Sum up counts for each column and divide to get probabilities
    percs = defaultdict(lambda: {})
    for (from_r, type), symbol_counts in counts.items():
        total = sum(symbol_counts.values())
        for symbol, cnt in symbol_counts.items():
            percs[from_r, type][symbol] = cnt / total
    return percs
```