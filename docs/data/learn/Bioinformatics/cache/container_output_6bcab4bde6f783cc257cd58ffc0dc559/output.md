`{bm-disable-all}`[ch9_code/src/sequence_search/Trie_EdgeMerged.py](ch9_code/src/sequence_search/Trie_EdgeMerged.py) (lines 137 to 162):`{bm-enable-all}`

```python
def find_sequence(
        data: str,
        end_marker: str,
        trie: Graph[str, None, str, str],
        root_nid: str
) -> tuple[int, str] | None:
    assert end_marker not in data, f'{data} should not have end marker'
    for start_idx in range(len(data)):
        nid = root_nid
        idx = start_idx
        while nid is not None:
            next_nid = None
            end_marker_reached = False
            for eid, _, to_nid, edge_str in trie.get_outputs_full(nid):
                if edge_str.endswith(end_marker):
                    end_marker_reached = True
                    edge_str = edge_str[:-1]
                edge_str_len = len(edge_str)
                if data[idx:idx + edge_str_len] == edge_str:
                    idx += edge_str_len
                    next_nid = to_nid
                    break
            if end_marker_reached:
                return idx, data[start_idx:idx]
            nid = next_nid
    return None
```