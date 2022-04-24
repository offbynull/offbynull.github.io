`{bm-disable-all}`[ch9_code/src/sequence_search/Trie_AhoCorasick.py](ch9_code/src/sequence_search/Trie_AhoCorasick.py) (lines 35 to 88):`{bm-enable-all}`

```python
def add_hop_edges(
        trie: Graph[str, None, str, str | None],
        root_nid: str,
        end_marker: str,
        hop_eid_gen: StringIdGenerator = StringIdGenerator('E_HOP')
):
    seqs = trie_to_sequences(trie, root_nid, end_marker)
    for seq in seqs:
        to_nid, cnt = trie_find_prefix(trie, root_nid, seq[1:])
        if to_nid == root_nid:
            continue
        from_nid, _ = trie_find_prefix(trie, root_nid, seq[:cnt+1])
        hop_already_exists = trie.has_outputs(from_nid, lambda _, __, n_to, ___: n_to == to_nid)
        if hop_already_exists:
            continue
        hop_eid = hop_eid_gen.next_id()
        trie.insert_edge(hop_eid, from_nid, to_nid)


def trie_find_prefix(
        trie: Graph[str, None, str, str | None],
        root_nid: str,
        value: str
) -> tuple[str, int]:
    nid = root_nid
    idx = 0
    while True:
        next_nid = None
        for _, _, to_nid, ed in trie.get_outputs_full(nid):
            if ed == value[idx]:
                idx += 1
                next_nid = to_nid
                break
        if next_nid is None:
            return nid, idx
        if idx == len(value):
            return next_nid, idx
        nid = next_nid


def trie_to_sequences(
        trie: Graph[str, None, str, str | None],
        nid: str,
        end_marker: str,
        current_val: str = ''
) -> set[str]:
    ret = set()
    for _, _, to_nid, ed in trie.get_outputs_full(nid):
        if ed == end_marker:
            ret.add(current_val)
            continue
        next_val = current_val + ed
        ret = ret | trie_to_sequences(trie, to_nid, end_marker, next_val)
    return ret
```