`{bm-disable-all}`[ch9_code/src/sequence_search/Trie_AhoCorasick.py](ch9_code/src/sequence_search/Trie_AhoCorasick.py) (lines 239 to 298):`{bm-enable-all}`

```python
def mismatch_search(
        test_seq: StringView,
        search_seqs: set[StringView],
        max_mismatch: int,
        end_marker: StringView,
        pad_marker: StringView
) -> tuple[
    Graph[str, None, str, StringView],
    set[tuple[int, StringView, StringView, int]]
]:
    # Add padding to test sequence
    assert end_marker not in test_seq, f'{test_seq} should not contain end marker'
    assert pad_marker not in test_seq, f'{test_seq} should not contain pad marker'
    padding = pad_marker * max_mismatch
    test_seq = padding + test_seq + padding
    # Generate seeds from search_seqs
    seed_to_seqs = defaultdict(set)
    seq_to_seeds = {}
    for seq in search_seqs:
        assert end_marker not in seq[-1], f'{seq} should not contain end marker'
        assert pad_marker not in seq, f'{seq} should not contain pad marker'
        seeds = to_seeds(seq, max_mismatch)
        seq_to_seeds[seq] = seeds
        for seed in seeds:
            seed_to_seqs[seed].add(seq)
    # Turn seeds into trie
    trie = to_trie(
        set(seed + end_marker for seed in seed_to_seqs),
        end_marker
    )
    # Scan for seeds
    found_set = set()
    found_seeds = find_sequence(
        test_seq,
        end_marker,
        trie,
        trie.get_root_node()
    )
    for found in found_seeds:
        found_idx, found_seed = found
        # Get all seqs that have this seed. The seed may appear more than once in a seq, so
        # perform "seed extension" for each occurrence.
        mapped_search_seqs = seed_to_seqs[found_seed]
        for search_seq in mapped_search_seqs:
            search_seq_seeds = seq_to_seeds[search_seq]
            for i, seed in enumerate(search_seq_seeds):
                if seed != found_seed:
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
    return trie, found_set
```