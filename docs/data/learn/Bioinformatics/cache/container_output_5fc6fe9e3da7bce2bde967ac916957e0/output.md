`{bm-disable-all}`[ch9_code/src/sequence_search/SuffixTree.py](ch9_code/src/sequence_search/SuffixTree.py) (lines 199 to 229):`{bm-enable-all}`

```python
def has_prefix(
        prefix: StringView,
        end_marker: str,
        suffix_tree: Graph[str, None, str, list[StringView]],
        root_nid: str
) -> bool:
    assert end_marker not in prefix, f'{prefix} should not have end marker'
    nid = root_nid
    while True:
        next_nid = None
        next_prefix_skip_count = 0
        for eid, _, to_nid, edge_strs in suffix_tree.get_outputs_full(nid):
            edge_str = edge_strs[0]  # any will work -- list is diff occurrences of same str
            # Strip off end marker (if present)
            if edge_str[-1] == end_marker:
                edge_str = edge_str[:-1]
            if len(edge_str) == 0:
                continue
            # Walk forward as much of the prefix as can be walked
            found_common_prefix_len = common_prefix_len(prefix, edge_str)
            if found_common_prefix_len > next_prefix_skip_count:
                next_prefix_skip_count = found_common_prefix_len
                if found_common_prefix_len == len(edge_str):
                    next_nid = to_nid
        prefix = prefix[next_prefix_skip_count:]
        if len(prefix) == 0:  # Has the prefix been fully consumed? If so, prefix is found.
            return True
        if next_nid is None:  # Otherwise, if there isn't a next node we can hop to, the prefix doesn't exist.
            return False
        nid = next_nid
```