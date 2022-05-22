`{bm-disable-all}`[ch9_code/src/sequence_search/Trie_AhoCorasick.py](ch9_code/src/sequence_search/Trie_AhoCorasick.py) (lines 131 to 168):`{bm-enable-all}`

```python
def find_sequence(
        data: StringView,
        end_marker: StringView,
        trie: Graph[str, None, str, StringView],
        root_nid: str
) -> tuple[int, str] | None:
    assert end_marker not in data, f'{data} should not have end marker'
    nid = root_nid
    skip_offset = 0
    for start_idx in range(len(data)):
        end_marker_found = False
        end_idx = start_idx
        for offset, ch in enumerate(data[start_idx + skip_offset:]):
            offset = offset + skip_offset
            # Find edge for ch
            found_nid = None
            end_marker_found = any(True for _, _, _, edge_ch in trie.get_outputs_full(nid) if edge_ch == end_marker)
            for _, _, to_nid, edge_ch in trie.get_outputs_full(nid):
                if edge_ch == ch:
                    found_nid = to_nid
                    end_idx = start_idx + offset
                    break
            # If found not found, use fast-forward edge if it exists or start from root if it doesn't
            if found_nid is None:
                hop_edge = trie.get_output_full(nid, lambda _, __, ___, edge_ch: edge_ch is None)
                if hop_edge is None:
                    nid = root_nid
                    skip_offset = 0
                else:
                    _, _, nid, _ = hop_edge
                    skip_offset = offset - 1
                break
            # Otherwise, keep going from the edge's end node
            nid = found_nid
        # End marker reached? Return with index of match and the match itself
        if end_marker_found:
            return start_idx, data[start_idx:end_idx+1]
    return None
```