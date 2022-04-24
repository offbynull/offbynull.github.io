from __future__ import annotations

from sys import stdin

import yaml

from graph.DirectedGraph import Graph
from graph.GraphHelpers import StringIdGenerator
from sequence_search import Trie_Basic


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
        if data is None:
            ret += f'{n1} -> {n2} [color=red, style=dashed]\n'
        else:
            ret += f'{n1} -> {n2} [label="{data}"]\n'
    ret += '}'
    return ret






# MARKDOWN_ADD_HOPS
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
# MARKDOWN_ADD_HOPS


# t = Trie_Basic.to_trie({'aratrium¶', 'aratron¶', 'ration¶'}, '¶')  # 'arations¶'
# print(f'{trie_find_prefix(t, "N0", "aratriux")}')
# add_hop_edges(t, 'N0', '¶')
# print(f'{to_dot(t)}')





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
        trie = Trie_Basic.to_trie(trie_seqs, end_marker)
        add_hop_edges(trie, trie.get_root_node(), end_marker)
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
    nid = root_nid
    skip_offset = 0
    for start_idx in range(len(data)):
        end_marker_found = False
        end_idx = start_idx
        for offset, ch in enumerate(data[start_idx + skip_offset:]):
            offset = offset + skip_offset
            # Find edge for ch
            found_nid = None
            end_marker_found = any(True for _, _, _, edge_ch in trie.get_outputs_full(nid) if edge_ch == end_marker)
            for _, _, to_nid, edge_ch in trie.get_outputs_full(nid):
                if edge_ch == ch:
                    found_nid = to_nid
                    end_idx = start_idx + offset
                    break
            # If found not found, use fast-forward edge if it exists or start from root if it doesn't
            if found_nid is None:
                hop_edge = trie.get_output_full(nid, lambda _, __, ___, edge_ch: edge_ch is None)
                if hop_edge is None:
                    nid = root_nid
                    skip_offset = 0
                else:
                    _, _, nid, _ = hop_edge
                    skip_offset = offset - 1
                break
            # Otherwise, keep going from the edge's end node
            nid = found_nid
        # End marker reached? Return with index of match and the match itself
        if end_marker_found:
            return start_idx, data[start_idx:end_idx+1]
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
        trie = Trie_Basic.to_trie(trie_seqs, end_marker)
        add_hop_edges(trie, trie.get_root_node(), end_marker)
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