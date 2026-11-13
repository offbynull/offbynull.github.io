`{bm-disable-all}`[ch9_code/src/sequence_search/SuffixArray.py](ch9_code/src/sequence_search/SuffixArray.py) (lines 174 to 226):`{bm-enable-all}`

```python
def mismatch_search(
        test_seq: StringView,
        search_seqs: set[StringView],
        max_mismatch: int,
        end_marker: StringView,
        pad_marker: StringView
) -> tuple[
    list[StringView],
    set[tuple[int, StringView, StringView, int]]
]:
    # Add end marker and padding to test sequence
    assert end_marker not in test_seq, f'{test_seq} should not contain end marker'
    assert pad_marker not in test_seq, f'{test_seq} should not contain pad marker'
    padding = pad_marker * max_mismatch
    test_seq = padding + test_seq + padding + end_marker
    # Turn test sequence into suffix tree
    array = to_suffix_array(test_seq, end_marker)
    # Generate seeds from search_seqs
    seed_to_seqs = defaultdict(set)
    seq_to_seeds = {}
    for seq in search_seqs:
        assert end_marker not in seq, f'{seq} should not contain end marker'
        assert pad_marker not in seq, f'{seq} should not contain pad marker'
        seeds = to_seeds(seq, max_mismatch)
        seq_to_seeds[seq] = seeds
        for seed in seeds:
            seed_to_seqs[seed].add(seq)
    # Scan for seeds
    found_set = set()
    for seed, mapped_search_seqs in seed_to_seqs.items():
        found_idxes = find_prefix(
            seed,
            end_marker,
            array
        )
        for found_idx in found_idxes:
            for search_seq in mapped_search_seqs:
                search_seq_seeds = seq_to_seeds[search_seq]
                for i, search_seq_seed in enumerate(search_seq_seeds):
                    if seed != search_seq_seed:
                        continue
                    se_res = seed_extension(test_seq, found_idx, i, search_seq_seeds)
                    if se_res is None:
                        continue
                    test_seq_idx, dist = se_res
                    if dist <= max_mismatch:
                        found_value = test_seq[test_seq_idx:test_seq_idx + len(search_seq)]
                        test_seq_idx_unpadded = test_seq_idx - len(padding)
                        found = test_seq_idx_unpadded, search_seq, found_value, dist
                        found_set.add(found)
                        break
    return array, found_set
```