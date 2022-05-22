from __future__ import annotations

from collections import defaultdict
from sys import stdin
from typing import TypeVar

import yaml

from graph.DirectedGraph import Graph
from graph.GraphHelpers import StringIdGenerator
from sequence_search import Trie_Basic
from sequence_search.SearchUtils import StringView, to_seeds, seed_extension


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
# MARKDOWN_ADD_HOPS


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
        data: StringView,
        end_marker: StringView,
        trie: Graph[str, None, str, StringView],
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
        trie_seqs = set(StringView.wrap(s) for s in data['trie_sequences'])
        test_seq = StringView.wrap(data['test_sequence'])
        end_marker = StringView.wrap(data['end_marker'])
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


# MARKDOWN_MISMATCH
def mismatch_search(
        test_seq: StringView,
        search_seqs: set[StringView],
        max_mismatch: int,
        end_marker: StringView
) -> tuple[
    Graph[str, None, str, StringView],
    set[tuple[int, StringView, StringView, int]]
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
    trie = Trie_Basic.to_trie(
        set(seed + end_marker for seed in seed_to_seqs),
        end_marker
    )
    add_hop_edges(trie, trie.get_root_node(), end_marker)
    # Scan for seeds
    found_set = set()
    offset = 0
    while offset < len(test_seq):
        # Search for seeds FROM offset (trim off the part of test_seq before offset)
        found = find_sequence(
            test_seq[offset:],
            end_marker,
            trie,
            trie.get_root_node()
        )
        if found is None:
            break
        found_idx, found_seed = found
        found_idx += offset  # Add the offset back into the found_idx
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
                    found = test_seq_idx, search_seq, found_value, dist
                    found_set.add(found)
                    break
        offset = found_idx + 1
    return trie, found_set
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
        trie, found_set = mismatch_search(test_seq, trie_seqs, max_mismatch, end_marker)
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
