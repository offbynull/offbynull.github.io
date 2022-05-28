from __future__ import annotations

import functools
from collections import defaultdict
from sys import stdin

import yaml

from sequence_search.SearchUtils import StringView, to_seeds, seed_extension


# MARKDOWN_BUILD
def cmp(a: StringView, b: StringView, end_marker: StringView):
    for a_ch, b_ch in zip(a, b):
        if a_ch == end_marker and b_ch == end_marker:
            continue
        if a_ch == end_marker:
            return -1
        if b_ch == end_marker:
            return 1
        if a_ch < b_ch:
            return -1
        if a_ch > b_ch:
            return 1
    if len(a) < len(b):
        return 1
    elif len(a) > len(b):
        return -1
    raise '???'


def to_suffix_array(
        seq: StringView,
        end_marker: StringView
):
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    ret = []
    while len(seq) > 0:
        ret.append(seq)
        seq = seq[1:]
    ret = sorted(ret, key=functools.cmp_to_key(lambda a, b: cmp(a, b, end_marker)))
    return ret
# MARKDOWN_BUILD


def main_build():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        seq = data['sequence']
        end_marker = data['end_marker']
        print(f'Building suffix array using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        array = to_suffix_array(
            StringView.wrap(seq),
            end_marker
        )
        print()
        print(f'The following suffix array was produced ...')
        print()
        print('```')
        for sv in array:
            print(f'{sv}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


def common_prefix_len(s1: StringView, s2: StringView):
    l = min(len(s1), len(s2))
    count = 0
    for i in range(l):
        if s1[i] == s2[i]:
            count += 1
        else:
            break
    return count


# MARKDOWN_TEST
def find_prefix(
        prefix: StringView,
        end_marker: StringView,
        suffix_array: list[StringView]
) -> list[int]:
    assert end_marker not in prefix, f'{prefix} should not have end marker'
    # Binary search
    start = 0
    end = len(suffix_array) - 1
    found = None
    while start <= end:
        mid = start + ((end - start) // 2)
        mid_suffix = suffix_array[mid]
        comparison = cmp(prefix, mid_suffix, end_marker)
        if common_prefix_len(prefix, mid_suffix) == len(prefix):
            found = mid
            break
        elif comparison < 0:
            end = mid - 1
        elif comparison > 0:
            start = mid + 1
        else:
            raise ValueError('This should never happen')
    # If not found, return
    if found is None:
        return []
    # Walk backward to see how many before start with prefix
    start = found
    while start >= 0:
        start_suffix = suffix_array[start]
        if common_prefix_len(prefix, start_suffix) != len(prefix):
            break
        start -= 1
    # Walk forward to see how many after start with prefix
    end = found + 1
    while end < len(suffix_array):
        end_suffix = suffix_array[end]
        if common_prefix_len(prefix, end_suffix) != len(prefix):
            break
        end += 1
    return [sv.start for sv in suffix_array[start:end]]
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
        print(f'Building suffix array using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        array = to_suffix_array(
            StringView.wrap(seq),
            end_marker
        )
        print()
        print(f'The following suffix array was produced ...')
        print()
        print('```')
        for sv in array:
            print(f'{sv}')
        print('```')
        print()
        found = find_prefix(
            StringView.wrap(prefix),
            end_marker,
            array
        )
        print()
        print(f'*{prefix}* found in *{seq}* at indices {found}')
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
    list[StringView],
    set[tuple[int, StringView, StringView, int]]
]:
    # Add end marker to test sequence
    assert end_marker not in test_seq, f'{test_seq} should not contain end marker'
    test_seq = test_seq + end_marker
    # Turn test sequence into suffix tree
    array = to_suffix_array(test_seq, end_marker)
    # Generate seeds from search_seqs
    seed_to_seqs = defaultdict(set)
    seq_to_seeds = {}
    for seq in search_seqs:
        assert end_marker not in seq, f'{seq} should not contain end marker'
        seeds = to_seeds(seq, max_mismatch)
        seq_to_seeds[seq] = seeds
        for seed in seeds:
            seed_to_seqs[seed].add(seq)
    # Scan for seeds
    found_set = set()
    for seed, mapped_search_seqs in seed_to_seqs.items():
        found_idxes = find_prefix(
            seed,
            end_marker,
            array
        )
        for found_idx in found_idxes:
            for search_seq in mapped_search_seqs:
                search_seq_seeds = seq_to_seeds[search_seq]
                for i, search_seq_seed in enumerate(search_seq_seeds):
                    if seed != search_seq_seed:
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
    return array, found_set
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
        array, found_set = mismatch_search(test_seq, trie_seqs, max_mismatch, end_marker)
        print()
        print(f'The following suffix array was produced ...')
        print()
        print('```')
        for sv in array:
            print(f'{sv}')
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
    main_build()
