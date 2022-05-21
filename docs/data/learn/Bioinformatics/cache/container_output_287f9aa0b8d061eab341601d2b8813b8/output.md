`{bm-disable-all}`[ch9_code/src/sequence_search/Trie_Basic.py](ch9_code/src/sequence_search/Trie_Basic.py) (lines 111 to 138):`{bm-enable-all}`

```python
def find_sequence(
        data: S,
        end_marker: str,
        trie: Graph[str, None, str, str],
        root_nid: str
) -> tuple[int, S] | None:
    assert end_marker not in data, f'{data} should not have end marker'
    for start_idx in range(len(data)):
        nid = root_nid
        end_idx = start_idx
        for idx, ch in enumerate(data[start_idx:]):
            # Find edge for ch
            found_nid = None
            for _, _, to_nid, edge_ch in trie.get_outputs_full(nid):
                if edge_ch == ch:
                    found_nid = to_nid
                    end_idx = start_idx + idx
                    break
            # If found not found, bail
            if found_nid is None:
                break
            # Otherwise, keep going from the edge's end node
            nid = found_nid
        # End marker reached? Return with index of match and the match itself
        end_marker_found = any(True for _, _, _, edge_ch in trie.get_outputs_full(nid) if edge_ch == end_marker)
        if end_marker_found:
            return start_idx, data[start_idx:end_idx+1]
    return None
```