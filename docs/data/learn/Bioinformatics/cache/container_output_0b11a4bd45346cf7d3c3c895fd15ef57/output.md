`{bm-disable-all}`[ch9_code/src/sequence_search/Trie_AhoCorasick.py](ch9_code/src/sequence_search/Trie_AhoCorasick.py) (lines 35 to 99):`{bm-enable-all}`

```python
def add_hop_edges(
        trie: Graph[str, None, str, StringView | None],
        root_nid: str,
        end_marker: StringView,
        hop_eid_gen: StringIdGenerator = StringIdGenerator('E_HOP')
):
    seqs = trie_to_sequences(trie, root_nid, end_marker)
    for seq in seqs:
        if len(seq) == 1:
            continue
        to_nid, cnt = trie_find_prefix(trie, root_nid, seq[1:])
        if to_nid == root_nid:
            continue
        from_nid, _ = trie_find_prefix(trie, root_nid, seq[:cnt+1])
        hop_already_exists = trie.has_outputs(from_nid, lambda _, __, n_to, ___: n_to == to_nid)
        if hop_already_exists:
            continue
        hop_eid = hop_eid_gen.next_id()
        trie.insert_edge(hop_eid, from_nid, to_nid)


def trie_to_sequences(
        trie: Graph[str, None, str, StringView | None],
        nid: str,
        end_marker: StringView,
        current_val: StringView | None = None
) -> set[StringView]:
    # On initial call, current_val will be set to None. Set it here based on what S is, where end_marker is
    # used to derive S.
    if current_val is None:
        if isinstance(end_marker, str):
            current_val = ''
        elif isinstance(end_marker, StringView):
            current_val = StringView.wrap('')
    # Build out sequences
    ret = set()
    for _, _, to_nid, edge_ch in trie.get_outputs_full(nid):
        if edge_ch == end_marker:
            ret.add(current_val)
            continue
        next_val = current_val + edge_ch
        ret = ret | trie_to_sequences(trie, to_nid, end_marker, next_val)
    return ret


def trie_find_prefix(
        trie: Graph[str, None, str, StringView | None],
        root_nid: str,
        value: StringView
) -> tuple[str, int]:
    nid = root_nid
    idx = 0
    while True:
        next_nid = None
        for _, _, to_nid, edge_ch in trie.get_outputs_full(nid):
            if edge_ch == value[idx]:
                idx += 1
                next_nid = to_nid
                break
        if next_nid is None:
            return nid, idx
        if idx == len(value):
            return next_nid, idx
        nid = next_nid
```