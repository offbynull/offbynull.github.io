`{bm-disable-all}`[ch9_code/src/sequence_search/Trie_Basic.py](ch9_code/src/sequence_search/Trie_Basic.py) (lines 108 to 141):`{bm-enable-all}`

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
    while next_idx < len(data):
        nid = root_nid
        end_idx = next_idx
        while end_idx < len(data):
            ch = data[end_idx]
            # Find edge for ch
            dst_nid = None
            for _, _, to_nid, edge_ch in trie.get_outputs_full(nid):
                if edge_ch == ch:
                    dst_nid = to_nid
                    break
            # If not found, bail
            if dst_nid is None:
                break
            # If found dst node points to end marker, store it
            found_end_marker = any(edge_ch == end_marker for _, _, _, edge_ch in trie.get_outputs_full(dst_nid))
            if found_end_marker:
                found_idx = next_idx
                found_str = data[next_idx:end_idx + 1]
                ret.add((found_idx, found_str))
            # Move forward
            nid = dst_nid
            end_idx += 1
        next_idx += 1
    return ret
```