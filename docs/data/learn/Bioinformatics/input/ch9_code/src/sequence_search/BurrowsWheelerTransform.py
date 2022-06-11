import functools
from collections import Counter

from helpers.Utils import rotate_right
from sequence_search.SearchUtils import StringView


# MARKDOWN_BUILD
def cmp(a: str, b: str, end_marker: str):
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


def to_bwt(
        seq: str,
        end_marker: str
):
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    rotations_with_counts = zip(
        rotate_right(seq),
        range(len(seq))
    )
    rotations_with_counts_sorted = sorted(
        rotations_with_counts,
        key=functools.cmp_to_key(lambda a, b: cmp(a[0], b[0], end_marker))
    )
    first_ch_counter = Counter()
    last_ch_counter = Counter()
    ret = []
    for i, (s, idx) in enumerate(rotations_with_counts_sorted):
        first_ch = s[0]
        first_ch_counter[first_ch] += 1
        first_ch_cnt = first_ch_counter[first_ch]
        last_ch = s[-1]
        last_ch_counter[last_ch] += 1
        last_ch_cnt = last_ch_counter[last_ch]
        ret.append([(first_ch, first_ch_cnt), (last_ch, last_ch_cnt), -1])
    for i in range(len(ret)):
        record = ret[i]
        last = record[1]
        for j, (first, _, _) in enumerate(ret):
            if last == first:
                record[2] = j
                break
    return ret  # first col, last col, last_to_first mapping
# MARKDOWN_BUILD


def exists(
        bwt_array: tuple[tuple[str, int], tuple[str, int], int],
        test: str
):
    for ch in reversed(test):
        [for first, last, last_to_first_idx in bwt_array if ch == last_ch]
    ...


res = to_bwt(
    'panamabananas$',
    '$'
)
for e in res:
    print(f'{e}')