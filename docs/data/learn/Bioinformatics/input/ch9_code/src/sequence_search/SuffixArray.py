from __future__ import annotations

import functools
from bisect import bisect_left, bisect_right
from sys import stdin

import yaml

from graph.DirectedGraph import Graph
from graph.GraphHelpers import StringIdGenerator


# MARKDOWN_BUILD
from sequence_search.SearchUtils import StringView


def cmp(a: StringView, b: StringView):
    end_marker = a.data[-1]
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
        end_marker: str
):
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    ret = []
    while len(seq) > 0:
        ret.append(seq)
        seq = seq[1:]
    ret = sorted(ret, key=functools.cmp_to_key(cmp))
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
def has_prefix(
        prefix: StringView,
        end_marker: str,
        suffix_array: list[StringView]
) -> bool:
    assert end_marker not in prefix, f'{prefix} should not have end marker'
    start = 0
    end = len(suffix_array)
    while start != end:
        mid = (end - start) // 2
        mid_suffix = suffix_array[mid]
        comparison = cmp(prefix, mid_suffix)
        if common_prefix_len(prefix, mid_suffix) == len(prefix):
            return True
        elif comparison < 0:
            end = mid
        elif comparison > 0:
            start = mid
        else:
            raise ValueError('This should never happen')
    return False
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
        found = has_prefix(
            StringView.wrap(prefix),
            end_marker,
            array
        )
        print()
        print(f'Was *{prefix}* found in *{seq}*: {found}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main_test()