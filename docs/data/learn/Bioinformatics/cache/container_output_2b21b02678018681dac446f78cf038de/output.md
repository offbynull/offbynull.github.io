`{bm-disable-all}`[ch9_code/src/sequence_search/SuffixTree.py](ch9_code/src/sequence_search/SuffixTree.py) (lines 33 to 112):`{bm-enable-all}`

```python
def to_suffix_tree(
        seq: StringView,
        end_marker: StringView,
        nid_gen: StringIdGenerator = StringIdGenerator('N'),
        eid_gen: StringIdGenerator = StringIdGenerator('E')
) -> Graph[str, None, str, list[StringView]]:
    tree = Graph()
    root_nid = nid_gen.next_id()
    tree.insert_node(root_nid)  # Insert root node
    while len(seq) > 0:
        add_suffix_to_tree(tree, root_nid, seq, end_marker, nid_gen, eid_gen)
        seq = seq[1:]
    return tree


def add_suffix_to_tree(
        trie: Graph[str, None, str, list[StringView]],
        root_nid: str,
        seq: StringView,
        end_marker: StringView,
        nid_gen: StringIdGenerator,
        eid_gen: StringIdGenerator
):
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    nid = root_nid
    while seq:
        # Find an edge with a prefix that extends from the current node
        found = None
        for eid, _, to_nid, edge_strs in trie.get_outputs_full(nid):
            edge_str = edge_strs[0]  # any will work -- list is diff occurrences of same str
            n = common_prefix_len(seq, edge_str)
            if n > 0:
                found = (to_nid, eid, edge_strs, n)
                break
        # If not found, add remainder of seq as an edge for current node and return
        if found is None:
            next_nid = nid_gen.next_id()
            next_eid = eid_gen.next_id()
            trie.insert_node(next_nid)
            trie.insert_edge(next_eid, nid, next_nid, [seq])
            return
        found_nid, found_eid, found_edge_strs, found_common_prefix_len = found
        found_edge_str_len = len(found_edge_strs[0])  # any will work -- list is diff occurrences of same str
        current_str_instance = seq[:found_common_prefix_len]
        # If the common prefix len is < the found edge string, break and extend from that edge, then return.
        if found_common_prefix_len < found_edge_str_len:
            break_nid = nid_gen.next_id()
            break_pre_eid = eid_gen.next_id()
            break_pre_strs = list(s[:found_common_prefix_len] for s in found_edge_strs)
            break_pre_strs.append(current_str_instance)
            break_post_eid = eid_gen.next_id()
            break_post_strs = list(s[found_common_prefix_len:] for s in found_edge_strs)
            trie.insert_node_between_edge(
                break_nid, None,
                found_eid,
                break_pre_eid, break_pre_strs,
                break_post_eid, break_post_strs
            )
            next_nid = nid_gen.next_id()
            next_eid = eid_gen.next_id()
            trie.insert_node(next_nid)
            remainder_str_instance = seq[found_common_prefix_len:]
            trie.insert_edge(next_eid, break_nid, next_nid, [remainder_str_instance])
            return
        # Otherwise, common prefix len is == the found edge string, so walk into that edge.
        found_edge_strs.append(current_str_instance)
        nid = found_nid
        seq = seq[found_common_prefix_len:]


def common_prefix_len(s1: StringView, s2: StringView):
    l = min(len(s1), len(s2))
    count = 0
    for i in range(l):
        if s1[i] == s2[i]:
            count += 1
        else:
            break
    return count
```