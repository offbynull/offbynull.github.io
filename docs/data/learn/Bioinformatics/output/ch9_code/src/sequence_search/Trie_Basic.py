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







# MARKDOWN_BUILD
def to_trie(
        seqs: set[StringView],
        end_marker: StringView,
        nid_gen: StringIdGenerator = StringIdGenerator('N'),
        eid_gen: StringIdGenerator = StringIdGenerator('E')
) -> Graph[str, None, str, StringView]:
    trie = Graph()
    root_nid = nid_gen.next_id()
    trie.insert_node(root_nid)  # Insert root node
    for seq in seqs:
        add_to_trie(trie, root_nid, seq, end_marker, nid_gen, eid_gen)
    return trie


def add_to_trie(
        trie: Graph[str, None, str, StringView],
        root_nid: str,
        seq: StringView,
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
        trie_seqs = set(StringView.wrap(s) for s in data['trie_sequences'])
        end_marker = StringView.wrap(data['end_marker'])
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
        end_idx = next_idx
        while end_idx < len(data):
            ch = data[end_idx]
            # Find edge for ch
            dst_nid = None
            for _, _, to_nid, edge_ch in trie.get_outputs_full(nid):
                if edge_ch == ch:
                    dst_nid = to_nid
                    break
            # If not found, bail
            if dst_nid is None:
                break
            # If found dst node points to end marker, store it
            found_end_marker = any(edge_ch == end_marker for _, _, _, edge_ch in trie.get_outputs_full(dst_nid))
            if found_end_marker:
                found_idx = next_idx
                found_str = data[next_idx:end_idx + 1]
                ret.add((found_idx, found_str))
            # Move forward
            nid = dst_nid
            end_idx += 1
        next_idx += 1
    return ret
# MARKDOWN_TEST


def main_test():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        trie_seqs = set(StringView.wrap(s) for s in data['trie_sequences'])
        test_seq = StringView.wrap(data['test_sequence'])
        end_marker = StringView.wrap(data['end_marker'])
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
        test_seq: StringView,
        search_seqs: set[StringView],
        max_mismatch: int,
        end_marker: StringView,
        pad_marker: StringView
) -> tuple[
    Graph[str, None, str, StringView],
    set[tuple[int, StringView, StringView, int]]
]:
    # Add padding to test sequence
    assert end_marker not in test_seq, f'{test_seq} should not contain end marker'
    assert pad_marker not in test_seq, f'{test_seq} should not contain pad marker'
    padding = pad_marker * max_mismatch
    test_seq = padding + test_seq + padding
    # Generate seeds from search_seqs
    seed_to_seqs = defaultdict(set)
    seq_to_seeds = {}
    for seq in search_seqs:
        assert end_marker not in seq[-1], f'{seq} should not contain end marker'
        assert pad_marker not in seq, f'{seq} should not contain pad marker'
        seeds = to_seeds(seq, max_mismatch)
        seq_to_seeds[seq] = seeds
        for seed in seeds:
            seed_to_seqs[seed].add(seq)
    # Turn seeds into trie
    trie = to_trie(
        set(seed + end_marker for seed in seed_to_seqs),
        end_marker
    )
    # Scan for seeds
    found_set = set()
    found_seeds = find_sequence(
        test_seq,
        end_marker,
        trie,
        trie.get_root_node()
    )
    for found in found_seeds:
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
                    found_value = test_seq[test_seq_idx:test_seq_idx + len(search_seq)]
                    test_seq_idx_unpadded = test_seq_idx - len(padding)
                    found = test_seq_idx_unpadded, search_seq, found_value, dist
                    found_set.add(found)
                    break
    return trie, found_set
# MARKDOWN_MISMATCH

def main_mismatch():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        trie_seqs = set(StringView.wrap(s) for s in data['trie_sequences'])
        test_seq = StringView.wrap(data['test_sequence'])
        end_marker = StringView.wrap(data['end_marker'])
        pad_marker = StringView.wrap(data['pad_marker'])
        max_mismatch = data['max_mismatch']
        print(f'Building and searching trie using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        trie, found_set = mismatch_search(test_seq, trie_seqs, max_mismatch, end_marker, pad_marker)
        print()
        print(f'The following trie was produced ...')
        print()
        print('```{dot}')
        print(f'{to_dot(trie)}')
        print('```')
        print()
        print(f'Searching `{test_seq}` with the trie revealed the following was found:')
        print()
        for found_idx, actual, found, dist in sorted(found_set):
            print(f' * Matched `{found}` against `{actual}` with distance of {dist} at index {found_idx}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main_mismatch()