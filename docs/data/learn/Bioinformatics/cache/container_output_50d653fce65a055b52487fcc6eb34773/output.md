`{bm-disable-all}`[ch9_code/src/sequence_search/Trie_EdgeMerged.py](ch9_code/src/sequence_search/Trie_EdgeMerged.py) (lines 141 to 188):`{bm-enable-all}`

```python
def find_sequence(
        data: S,
        end_marker: str,
        trie: Graph[str, None, str, S],
        root_nid: str
) -> tuple[int, str] | None:
    assert end_marker not in data, f'{data} should not have end marker'
    for start_idx in range(len(data)):
        nid = root_nid
        idx = start_idx
        while nid is not None:
            next_nid = None
            found_end_marker = False
            found_edge_str = None
            found_edge_str_len = -1
            for eid, _, to_nid, edge_str in trie.get_outputs_full(nid):
                end_marker_present = edge_str[-1] == end_marker
                if end_marker_present:
                    edge_str = edge_str[:-1]
                edge_str_len = len(edge_str)
                # The condition (edge_str_len > found_edge_str_len) ensures that if there are multiple edges but one of
                # them is just an edge with an end marker, that "end marker" edge is only taken if there isn't an edge
                # with some characters in it already. Imagine the following tree...
                #
                #   $
                # .---->*
                # | an    n$
                # *---->*----->*
                #       |  $
                #       '----->*
                #
                # If you use that trie to search the string "annoys", it would first go down the "an" edge and then have
                # the option of going down "n$" or "$". Without the condition (edge_str_len > found_edge_str_len), if
                # the graph returned edge "n$" and then "$", you would only match up to "[an]noys" instead of "[ann]oys"
                if data[idx:idx + edge_str_len] == edge_str and edge_str_len > found_edge_str_len:
                    next_nid = to_nid
                    if end_marker_present:
                        found_end_marker = True
                    found_edge_str = edge_str
                    found_edge_str_len = edge_str_len
            idx += found_edge_str_len
            # The condition (start_idx != idx) ensures that something other than empty string was captured. This is
            # needed because root extends an edge with just the edge marker which we don't want to match on (the edge
            # marker isn't included, which is why it's checking for empty string)
            if found_end_marker and start_idx != idx:
                return start_idx, data[start_idx:idx]
            nid = next_nid
    return None
```