from __future__ import annotations

from collections import defaultdict
from sys import stdin
from typing import TypeVar

import yaml

from graph.DirectedGraph import Graph
from graph.GraphHelpers import StringIdGenerator
from sequence_search.SearchUtils import to_seeds, seed_extension, StringView


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







S = TypeVar('S', StringView, str)


# MARKDOWN_BUILD
def to_trie(
        seqs: set[S],
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


def add_to_trie(
        trie: Graph[str, None, str, str],
        root_nid: str,
        seq: S,
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
        data: S,
        end_marker: str,
        trie: Graph[str, None, str, str],
        root_nid: str
) -> tuple[int, S] | None:
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
        print(f'Searching `{test_seq}` with the trie revealed the following was found: {found}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")



# MARKDOWN_MISMATCH
def mismatch_search(
        test_seq: S,
        search_seqs: set[S],
        max_mismatch: int,
        end_marker: str
) -> tuple[
    Graph[str, None, str, str],
    list[tuple[int, S, S, int]]
]:
    # Generate seeds from search_seqs
    seed_to_seqs = defaultdict(set)
    seq_to_seeds = {}
    for seq in search_seqs:
        assert end_marker == seq[-1], f'{seq} missing end marker'
        seq_no_marker = seq[:-1]
        seeds = to_seeds(seq_no_marker, max_mismatch)
        seq_to_seeds[seq_no_marker] = seeds
        for seed in seeds:
            seed_to_seqs[seed].add(seq_no_marker)
    # Turn seeds into trie
    trie = to_trie(
        set(seed + end_marker for seed in seed_to_seqs),
        end_marker
    )
    # Scan for seeds
    found_list = []
    test_seq_offset = 0
    while len(test_seq) > 0:
        # Search for seeds
        found = find_sequence(
            test_seq,
            end_marker,
            trie,
            trie.get_root_node()
        )
        if found is None:
            break
        found_idx, found_seed = found
        # Get all seqs that have this seed. The seed may appear more than once in a seq, so
        # perform "seed extension" for each occurrence.
        mapped_search_seqs = seed_to_seqs[found_seed]
        for search_seq in mapped_search_seqs:
            search_seq_seeds = seq_to_seeds[search_seq]
            for i, seed in enumerate(search_seq_seeds):
                if seed != found_seed:
                    continue
                se_res = seed_extension(test_seq, found_idx, i, search_seq_seeds)
                if se_res is None:
                    continue
                test_seq_idx, dist = se_res
                if dist <= max_mismatch:
                    found_value = test_seq[found_idx:found_idx + len(search_seq)]
                    found_list.append((test_seq_offset + found_idx, search_seq, found_value, dist))
        test_seq = test_seq[found_idx + 1:]
        test_seq_offset += found_idx + 1
    return trie, found_list
# MARKDOWN_MISMATCH


def main_mismatch():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        trie_seqs = set(data['trie_sequences'])
        test_seq = data['test_sequence']
        end_marker = data['end_marker']
        max_mismatch = data['max_mismatch']
        print(f'Building and searching trie using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        trie, found_list = mismatch_search(test_seq, trie_seqs, max_mismatch, end_marker)
        print()
        print(f'The following trie was produced ...')
        print()
        print('```{dot}')
        print(f'{to_dot(trie)}')
        print('```')
        print()
        print(f'Searching `{test_seq}` with the trie revealed the following was found:')
        print()
        for found_idx, actual, found, dist in found_list:
            print(f' * Matched `{found}` against `{actual}` with distance of {dist} at index {found_idx}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main_mismatch()