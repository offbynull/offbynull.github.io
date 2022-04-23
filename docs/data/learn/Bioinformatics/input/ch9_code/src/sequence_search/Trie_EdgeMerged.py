from __future__ import annotations

from sys import stdin

import yaml

from graph.DirectedGraph import Graph
from graph.GraphHelpers import StringIdGenerator


def to_dot(g: Graph) -> str:
    ret = 'digraph G {\n'
    ret += ' rankdir=LR\n'
    ret += ' node[fontname="Courier-Bold", fontsize=10, shape=point]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    for n in sorted(g.get_nodes()):
        data = g.get_node_data(n)
        ret += f'{n} [label=""]\n'
    for e in sorted(g.get_edges()):
        n1, n2, data = g.get_edge(e)
        ret += f'{n1} -> {n2} [label="{data}"]\n'
    ret += '}'
    return ret










def to_trie(
        seqs: set[str],
        end_marker: str,
        nid_gen: StringIdGenerator = StringIdGenerator('N'),
        eid_gen: StringIdGenerator = StringIdGenerator('E')
) -> Graph[str, None, str, str]:
    trie = Graph()
    root_nid = nid_gen.next_id()
    trie.insert_node(root_nid)  # Insert root node
    for seq in seqs:
        add_to_trie(trie, root_nid, seq, end_marker, nid_gen, eid_gen)
    return trie


# MARKDOWN_BUILD
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
    while seq:
        # Find an edge with a prefix that extends from the current node
        found = None
        for eid, _, to_nid, edge_str in trie.get_outputs_full(nid):
            n = common_prefix_len(seq, edge_str)
            if n > 0:
                found = (to_nid, eid, edge_str, n)
                break
        # If not found, add remainder of seq as an edge for current node and return
        if found is None:
            next_nid = nid_gen.next_id()
            next_eid = eid_gen.next_id()
            trie.insert_node(next_nid)
            trie.insert_edge(next_eid, nid, next_nid, seq)
            return
        found_nid, found_eid, found_edge_str, found_common_prefix_len = found
        # If the common prefix len is < the found edge string, break and extend from that edge, then return.
        if found_common_prefix_len < len(found_edge_str):
            break_nid = nid_gen.next_id()
            break_pre_eid = eid_gen.next_id()
            break_post_eid = eid_gen.next_id()
            trie.insert_node_between_edge(
                break_nid, None,
                found_eid,
                break_pre_eid, found_edge_str[:found_common_prefix_len],
                break_post_eid, found_edge_str[found_common_prefix_len:]
            )
            next_nid = nid_gen.next_id()
            next_eid = eid_gen.next_id()
            trie.insert_node(next_nid)
            trie.insert_edge(next_eid, break_nid, next_nid, seq[found_common_prefix_len:])
            return
        # Otherwise, common prefix len is == the found edge string, so walk into that edge.
        nid = found_nid
        seq = seq[found_common_prefix_len:]


def common_prefix_len(s1: str, s2: str):
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
        trie_seqs = data['trie_sequences']
        end_marker = data['end_marker']
        print(f'Building trie using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        trie = to_trie(trie_seqs, end_marker)
        print()
        print(f'The following trie was produced ...')
        print()
        print('```{dot}')
        print(f'{to_dot(trie)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


# MARKDOWN_TEST
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
# MARKDOWN_TEST


def main_test():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        trie_seqs = data['trie_sequences']
        test_seq = data['test_sequence']
        end_marker = data['end_marker']
        print(f'Building and searching trie using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        trie = to_trie(trie_seqs, end_marker)
        print()
        print(f'The following trie was produced ...')
        print()
        print('```{dot}')
        print(f'{to_dot(trie)}')
        print('```')
        print()
        found = find_sequence(test_seq, end_marker, trie, trie.get_root_node())
        print()
        print(f'Searching *{test_seq}* with the trie revealed the following was found: {found}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main_test()