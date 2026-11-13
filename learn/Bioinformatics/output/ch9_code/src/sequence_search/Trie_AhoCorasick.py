from __future__ import annotations

from collections import defaultdict
from sys import stdin

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
def to_trie(
        seqs: set[StringView],
        end_marker: StringView,
        nid_gen: StringIdGenerator = StringIdGenerator('N'),
        eid_gen: StringIdGenerator = StringIdGenerator('E')
) -> Graph[str, None, str, StringView | None]:
    trie = Trie_Basic.to_trie(
        seqs,
        end_marker,
        nid_gen,
        eid_gen
    )
    add_hop_edges(trie, trie.get_root_node(), end_marker)
    return trie


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
    hop_nid = None
    hop_offset = None
    while next_idx < len(data):
        nid = root_nid if hop_nid is None else hop_nid
        end_idx = next_idx + (0 if hop_offset is None else hop_offset)
        # If, on the last iteration, we followed a hop edge (hop_offset is not None), end_idx will be > next_idx.
        # Following a hop edge means that we've "fast-forwarded" movement in the trie. If the "fast-forwarded" position
        # we're starting at has an edge pointing to an end-marker, immediately put it into the return set.
        if next_idx != end_idx:
            pull_substring_if_end_marker_found(data, end_marker, trie, nid, next_idx, end_idx, ret)
        hop_offset = None
        while end_idx < len(data):
            ch = data[end_idx]
            # Find edge for ch
            dst_nid = None
            for _, _, to_nid, edge_ch in trie.get_outputs_full(nid):
                if edge_ch == ch:
                    dst_nid = to_nid
                    break
            # If not found, bail (hopping forward by setting hop_offset / next_nid if a hop edge is present)
            if dst_nid is None:
                hop_nid = next(
                    (to_nid for _, _, to_nid, edge_ch in trie.get_outputs_full(nid) if edge_ch is None),
                    None
                )
                if hop_nid is not None:
                    hop_offset = end_idx - next_idx - 1
                break
            # Move forward, and, if there's an edge pointing to an end-marker, put it in the return set.
            nid = dst_nid
            end_idx += 1
            pull_substring_if_end_marker_found(data, end_marker, trie, nid, next_idx, end_idx, ret)
        next_idx = next_idx + (1 if hop_offset is None else hop_offset)
    return ret


def pull_substring_if_end_marker_found(
        data: StringView,
        end_marker: StringView,
        trie: Graph[str, None, str, StringView],
        nid: str,
        next_idx: int,
        end_idx: int,
        container: set[tuple[int, StringView]]
):
    found_end_marker = any(edge_ch == end_marker for _, _, _, edge_ch in trie.get_outputs_full(nid))
    if found_end_marker:
        found_idx = next_idx
        found_str = data[found_idx:end_idx]
        container.add((found_idx, found_str))
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
        print(f'Searching *{test_seq}* with the trie revealed the following was found: {found}')
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
    main_test()
