from __future__ import annotations

from collections import defaultdict
from sys import stdin
from typing import TypeVar

import yaml

from graph.DirectedGraph import Graph
from graph.GraphHelpers import StringIdGenerator
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
        end_marker: StringView,
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
        data: StringView,
        end_marker: StringView,
        trie: Graph[str, None, str, StringView],
        root_nid: str
) -> tuple[int, StringView] | None:
    assert end_marker not in data, f'{data} should not have end marker'
    for start_idx in range(len(data)):
        nid = root_nid
        idx = start_idx
        while nid is not None:
            next_nid = None
            found_end_marker = False
            found_edge_str = None
            found_edge_str_len = -1
            for eid, _, to_nid, edge_str in trie.get_outputs_full(nid):
                end_marker_present = edge_str[-1] == end_marker
                if end_marker_present:
                    edge_str = edge_str[:-1]
                edge_str_len = len(edge_str)
                # The condition (edge_str_len > found_edge_str_len) ensures that if there are multiple edges but one of
                # them is just an edge with an end marker, that "end marker" edge is only taken if there isn't an edge
                # with some characters in it already. Imagine the following tree...
                #
                #   $
                # .---->*
                # | an    n$
                # *---->*----->*
                #       |  $
                #       '----->*
                #
                # If you use that trie to search the string "annoys", it would first go down the "an" edge and then have
                # the option of going down "n$" or "$". Without the condition (edge_str_len > found_edge_str_len), if
                # the graph returned edge "n$" and then "$", you would only match up to "[an]noys" instead of "[ann]oys"
                if data[idx:idx + edge_str_len] == edge_str and edge_str_len > found_edge_str_len:
                    next_nid = to_nid
                    if end_marker_present:
                        found_end_marker = True
                    found_edge_str = edge_str
                    found_edge_str_len = edge_str_len
            idx += found_edge_str_len
            # The condition (start_idx != idx) ensures that something other than empty string was captured. This is
            # needed because root extends an edge with just the edge marker which we don't want to match on (the edge
            # marker isn't included, which is why it's checking for empty string)
            if found_end_marker and start_idx != idx:
                return start_idx, data[start_idx:idx]
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
    FIX ME
    FIX ME
    FIX ME
    FIX ME
    FIX ME
    FIX ME
    FIX ME
    FIX ME
    FIX ME
    FIX ME
    FIX ME
    assert end_marker not in test_seq, f'{test_seq} should not contain end marker'
    # Generate seeds from search_seqs
    seed_to_seqs = defaultdict(set)
    seq_to_seeds = {}
    for seq in search_seqs:
        assert end_marker not in seq[-1], f'{seq} should not contain end marker'
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
        trie_seqs = set(StringView.wrap(s) for s in data['trie_sequences'])
        test_seq = StringView.wrap(data['test_sequence'])
        end_marker = StringView.wrap(data['end_marker'])
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
