`{bm-disable-all}`[ch9_code/src/sequence_search/SuffixTree.py](ch9_code/src/sequence_search/SuffixTree.py) (lines 224 to 269):`{bm-enable-all}`

```python
def mismatch_search(
        test_seq: StringView,
        search_seqs: set[StringView],
        max_mismatch: int,
        end_marker: StringView
) -> tuple[
    Graph[str, None, str, list[StringView]],
    set[tuple[int, StringView, StringView, int]]
]:
    # Turn test sequence into suffix tree
    trie = to_suffix_tree(test_seq, end_marker)
    # Generate seeds from search_seqs
    seed_to_seqs = defaultdict(set)
    seq_to_seeds = {}
    for seq in search_seqs:
        assert end_marker not in seq, f'{seq} should not contain end marker'
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
            trie,
            trie.get_root_node()
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
                        found = test_seq_idx, search_seq, found_value, dist
                        found_set.add(found)
                        break
    return trie, found_set
```