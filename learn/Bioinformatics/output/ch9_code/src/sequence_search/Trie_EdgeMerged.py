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
