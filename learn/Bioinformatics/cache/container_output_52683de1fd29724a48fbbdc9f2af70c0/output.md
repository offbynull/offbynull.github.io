`{bm-disable-all}`[ch9_code/src/sequence_search/Trie_EdgeMerged.py](ch9_code/src/sequence_search/Trie_EdgeMerged.py) (lines 138 to 196):`{bm-enable-all}`

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
        idx = next_idx
        while nid is not None:
            next_nid = None
            found_edge_str_len = -1
            # If an edge matches, there's a special case that needs to be handled where the edge just contains the
            # end marker. For example, consider the following edge merged trie (end marker is $) ...
            #
            #                o$
            #             .----->*
            #   an     n  |  $
            # *---->*----->*---->*
            #       |  $
            #       '----->*
            #
            # If you use this trie to search the string "annoys", it would first go down the "an" and then have the
            # option of going down "n" or "$"...
            #
            #  * For edge "n", there's an "n" after the "an" in "annoy", meaning this path should be chosen to
            #    continue the search.
            #  * For edge "$", the "$" by itself means that all the preceding text was something being looked for,
            #    meaning that "an" gets added to the return set as a found item.
            #
            # Ultimately, the trie above should match "[an]noys", "[ann]oys", and "[anno]ys".
            found_end_marker_only_edge = any(edge_str == end_marker for _, _, _, edge_str in trie.get_outputs_full(nid))
            if found_end_marker_only_edge:
                found_idx = next_idx
                found_str = data[next_idx:idx]
                ret.add((found_idx, found_str))
            for eid, _, to_nid, edge_str in trie.get_outputs_full(nid):
                found_edge_str_end_marker = edge_str[-1] == end_marker
                if found_edge_str_end_marker:
                    edge_str = edge_str[:-1]
                    if len(edge_str) == 0:
                        continue  # This edge had just the edge marker by itself -- skip as it was already handled above
                edge_str_len = len(edge_str)
                end_idx = idx + edge_str_len
                if edge_str == data[idx:end_idx]:
                    next_nid = to_nid
                    found_edge_str_len = edge_str_len
                    if found_edge_str_end_marker:
                        found_idx = next_idx
                        found_str = data[next_idx:end_idx]
                        ret.add((found_idx, found_str))
                    break
            idx += found_edge_str_len
            nid = next_nid
        next_idx += 1
    return ret
```