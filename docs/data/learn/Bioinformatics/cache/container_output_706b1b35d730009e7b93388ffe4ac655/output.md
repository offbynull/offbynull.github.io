`{bm-disable-all}`[ch9_code/src/sequence_search/Trie_AhoCorasick.py](ch9_code/src/sequence_search/Trie_AhoCorasick.py) (lines 145 to 204):`{bm-enable-all}`

```python
def find_sequence(
        data: StringView,
        end_marker: StringView,
        trie: Graph[str, None, str, StringView],
        root_nid: str
) -> set[tuple[int, StringView]]:
    assert end_marker not in data, f'{data} should not have end marker'
    ret = set()
    next_idx = 0
    hop_nid = None
    hop_offset = None
    while next_idx < len(data):
        nid = root_nid if hop_nid is None else hop_nid
        end_idx = next_idx + (0 if hop_offset is None else hop_offset)
        # If, on the last iteration, we followed a hop edge (hop_offset is not None), end_idx will be > next_idx.
        # Following a hop edge means that we've "fast-forwarded" movement in the trie. If the "fast-forwarded" position
        # we're starting at has an edge pointing to an end-marker, immediately put it into the return set.
        if next_idx != end_idx:
            pull_substring_if_end_marker_found(data, end_marker, trie, nid, next_idx, end_idx, ret)
        hop_offset = None
        while end_idx < len(data):
            ch = data[end_idx]
            # Find edge for ch
            dst_nid = None
            for _, _, to_nid, edge_ch in trie.get_outputs_full(nid):
                if edge_ch == ch:
                    dst_nid = to_nid
                    break
            # If not found, bail (hopping forward by setting hop_offset / next_nid if a hop edge is present)
            if dst_nid is None:
                hop_nid = next(
                    (to_nid for _, _, to_nid, edge_ch in trie.get_outputs_full(nid) if edge_ch is None),
                    None
                )
                if hop_nid is not None:
                    hop_offset = end_idx - next_idx - 1
                break
            # Move forward, and, if there's an edge pointing to an end-marker, put it in the return set.
            nid = dst_nid
            end_idx += 1
            pull_substring_if_end_marker_found(data, end_marker, trie, nid, next_idx, end_idx, ret)
        next_idx = next_idx + (1 if hop_offset is None else hop_offset)
    return ret


def pull_substring_if_end_marker_found(
        data: StringView,
        end_marker: StringView,
        trie: Graph[str, None, str, StringView],
        nid: str,
        next_idx: int,
        end_idx: int,
        container: set[tuple[int, StringView]]
):
    found_end_marker = any(edge_ch == end_marker for _, _, _, edge_ch in trie.get_outputs_full(nid))
    if found_end_marker:
        found_idx = next_idx
        found_str = data[found_idx:end_idx]
        container.add((found_idx, found_str))
```