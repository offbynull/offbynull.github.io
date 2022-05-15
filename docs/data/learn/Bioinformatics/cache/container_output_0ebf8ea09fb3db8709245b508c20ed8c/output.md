`{bm-disable-all}`[ch9_code/src/sequence_search/Trie_Basic.py](ch9_code/src/sequence_search/Trie_Basic.py) (lines 51 to 79):`{bm-enable-all}`

```python
def add_to_trie(
        trie: Graph[str, None, str, str],
        root_nid: str,
        seq: str,
        end_marker: str,
        nid_gen: StringIdGenerator,
        eid_gen: StringIdGenerator
):
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    nid = root_nid
    for ch in seq:
        # Find edge for ch
        found_nid = None
        for _, _, to_nid, edge_ch in trie.get_outputs_full(nid):
            if ch == edge_ch:
                found_nid = to_nid
                break
        # If found, use that edge's end node as the start of the next iteration
        if found_nid is not None:
            nid = found_nid
            continue
        # Otherwise, add the missing edge for ch
        next_nid = nid_gen.next_id()
        next_eid = eid_gen.next_id()
        trie.insert_node(next_nid)
        trie.insert_edge(next_eid, nid, next_nid, ch)
        nid = next_nid
```