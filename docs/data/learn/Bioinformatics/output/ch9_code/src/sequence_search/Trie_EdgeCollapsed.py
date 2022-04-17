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










# MARKDOWN_BUILD
def to_trie(
        seqs: set[str],
        end_marker: str,
        nid_gen: StringIdGenerator = StringIdGenerator('N'),
        eid_gen: StringIdGenerator = StringIdGenerator('E')
) -> Graph[str, None, str, str]:
    for seq in seqs:
        assert end_marker == seq[-1], f'{seq} missing end marker'
        assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    trie = Graph()
    root_nid = nid_gen.next_id()
    trie.insert_node(root_nid)  # Insert root node
    for seq in seqs:
        add_to_trie(trie, root_nid, seq, nid_gen, eid_gen)
    return trie


def add_to_trie(
        trie: Graph[str, None, str, str],
        root_nid: str,
        seq: str,
        nid_gen: StringIdGenerator,
        eid_gen: StringIdGenerator):
    nid = root_nid
    while seq:
        found_nid, found_prefix = find_prefix_from_node(trie, nid, seq)
        if found_nid is not None:
            nid = found_nid
            seq = seq[len(found_prefix):]
            continue
        # Otherwise, add the missing edge for ch
        next_nid = nid_gen.next_id()
        next_eid = eid_gen.next_id()
        trie.insert_node(next_nid)
        trie.insert_edge(next_eid, nid, next_nid, seq)
        nid = next_nid


def find_prefix_from_node(
        trie: Graph[str, None, str, str],
        nid: str,
        val: str
):
    for _, _, to_nid, edge_str in trie.get_outputs_full(nid):
        if val.startswith(edge_str):
            return to_nid, edge_str
    return None, None

TODO: THE CODE ABOVE IS WRONG. FIX IT AND PLUG IT INTO MARKDOWN
TODO: THE CODE ABOVE IS WRONG. FIX IT AND PLUG IT INTO MARKDOWN
TODO: THE CODE ABOVE IS WRONG. FIX IT AND PLUG IT INTO MARKDOWN
TODO: THE CODE ABOVE IS WRONG. FIX IT AND PLUG IT INTO MARKDOWN
TODO: THE CODE ABOVE IS WRONG. FIX IT AND PLUG IT INTO MARKDOWN
TODO: THE CODE ABOVE IS WRONG. FIX IT AND PLUG IT INTO MARKDOWN
TODO: THE CODE ABOVE IS WRONG. FIX IT AND PLUG IT INTO MARKDOWN
TODO: THE CODE ABOVE IS WRONG. FIX IT AND PLUG IT INTO MARKDOWN
TODO: THE CODE ABOVE IS WRONG. FIX IT AND PLUG IT INTO MARKDOWN
TODO: THE CODE ABOVE IS WRONG. FIX IT AND PLUG IT INTO MARKDOWN
TODO: THE CODE ABOVE IS WRONG. FIX IT AND PLUG IT INTO MARKDOWN
TODO: THE CODE ABOVE IS WRONG. FIX IT AND PLUG IT INTO MARKDOWN
TODO: THE CODE ABOVE IS WRONG. FIX IT AND PLUG IT INTO MARKDOWN
TODO: THE CODE ABOVE IS WRONG. FIX IT AND PLUG IT INTO MARKDOWN
TODO: THE CODE ABOVE IS WRONG. FIX IT AND PLUG IT INTO MARKDOWN
TODO: THE CODE ABOVE IS WRONG. FIX IT AND PLUG IT INTO MARKDOWN
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
        end_idx = start_idx
        for idx, ch in enumerate(data[start_idx:]):
            # Find edge for ch
            found_nid = None
            for _, _, to_nid, edge_ch in trie.get_outputs_full(nid):
                if edge_ch == ch:
                    found_nid = to_nid
                    end_idx = start_idx + idx
                    break
            # If found not found, bail
            if found_nid is None:
                break
            # Otherwise, keep going from the edge's end node
            nid = found_nid
        # End marker reached? Return with index of match and the match itself
        end_marker_found = any(True for _, _, _, edge_ch in trie.get_outputs_full(nid) if edge_ch == end_marker)
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