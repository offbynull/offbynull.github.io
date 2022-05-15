from __future__ import annotations

from sys import stdin

import yaml

from graph.DirectedGraph import Graph
from graph.GraphHelpers import StringIdGenerator
from sequence_search.SearchUtils import StringView


def to_dot(g: Graph[str, None, str, list[StringView]]) -> str:
    ret = 'digraph G {\n'
    ret += ' rankdir=LR\n'
    ret += ' node[fontname="Courier-Bold", fontsize=10, shape=point]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    for n in sorted(g.get_nodes()):
        data = g.get_node_data(n)
        ret += f'{n} [label=""]\n'
    for e in sorted(g.get_edges()):
        n1, n2, data = g.get_edge(e)
        data_str = str(data[0])  # all views are the same, just different instances -- any will work
        ranges_str = '\\n'.join(f"[{r.start}, {r.stop})" for r in data)
        ret += f'{n1} -> {n2} [label="{data_str}\\n{ranges_str}"]\n'
    ret += '}'
    return ret




# MARKDOWN_BUILD
def to_suffix_tree(
        seq: StringView,
        end_marker: str,
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
        end_marker: str,
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
# MARKDOWN_BUILD


def main_build():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        seq = data['sequence']
        end_marker = data['end_marker']
        print(f'Building suffix tree using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        tree = to_suffix_tree(
            StringView.wrap(seq),
            end_marker
        )
        print()
        print(f'The following suffix tree was produced ...')
        print()
        print('```{dot}')
        print(f'{to_dot(tree)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


# MARKDOWN_TEST
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
# MARKDOWN_TEST


def main_test():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        prefix = data['prefix']
        seq = data['sequence']
        end_marker = data['end_marker']
        print(f'Building and searching suffix tree using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        tree = to_suffix_tree(
            StringView.wrap(seq),
            end_marker
        )
        print()
        print(f'The following suffix tree was produced ...')
        print()
        print('```{dot}')
        print(f'{to_dot(tree)}')
        print('```')
        print()
        found = has_prefix(
            StringView.wrap(prefix),
            end_marker,
            tree,
            tree.get_root_node()
        )
        print()
        print(f'Was *{prefix}* found in *{seq}*: {found}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main_test()