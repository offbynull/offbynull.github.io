`{bm-disable-all}`[ch9_code/src/sequence_search/Trie_AhoCorasick.py](ch9_code/src/sequence_search/Trie_AhoCorasick.py) (lines 205 to 264):`{bm-enable-all}`

```python
def mismatch_search(
        test_seq: StringView,
        search_seqs: set[StringView],
        max_mismatch: int,
        end_marker: StringView
) -> tuple[
    Graph[str, None, str, StringView],
    set[tuple[int, StringView, StringView, int]]
]:
    # Generate seeds from search_seqs
    seed_to_seqs = defaultdict(set)
    seq_to_seeds = {}
    for seq in search_seqs:
        assert end_marker == seq[-1], f'{seq} missing end marker'
        seq_no_marker = seq[:-1]
        seeds = to_seeds(seq_no_marker, max_mismatch)
        seq_to_seeds[seq_no_marker] = seeds
        for seed in seeds:
            seed_to_seqs[seed].add(seq_no_marker)
    # Turn seeds into trie
    trie = Trie_Basic.to_trie(
        set(seed + end_marker for seed in seed_to_seqs),
        end_marker
    )
    add_hop_edges(trie, trie.get_root_node(), end_marker)
    # Scan for seeds
    found_set = set()
    offset = 0
    while offset < len(test_seq):
        # Search for seeds FROM offset (trim off the part of test_seq before offset)
        found = find_sequence(
            test_seq[offset:],
            end_marker,
            trie,
            trie.get_root_node()
        )
        if found is None:
            break
        found_idx, found_seed = found
        found_idx += offset  # Add the offset back into the found_idx
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
                    found = test_seq_idx, search_seq, found_value, dist
                    found_set.add(found)
                    break
        offset = found_idx + 1
    return trie, found_set
```