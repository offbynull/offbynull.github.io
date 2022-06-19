import functools
from collections import Counter

from helpers.Utils import rotate_right
from sequence_search import SuffixArray
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


class BWTRecord:
    __slots__ = ['first_ch', 'first_ch_idx', 'last_ch', 'last_ch_idx', 'last_to_first_idx']

    def __init__(self, first_ch: str, first_ch_idx: int, last_ch: str, last_ch_idx: int):
        self.first_ch = first_ch
        self.first_ch_idx = first_ch_idx
        self.last_ch = last_ch
        self.last_ch_idx = last_ch_idx
        self.last_to_first_idx = -1

    def __str__(self):
        return str((self.first_ch + str(self.first_ch_idx), self.last_ch + str(self.last_ch_idx), self.last_to_first_idx))

    def __repr__(self):
        return str(self)


def to_bwt(
        seq: str,
        end_marker: str
) -> list[BWTRecord]:
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
        first_ch_idx = first_ch_counter[first_ch]
        last_ch = s[-1]
        last_ch_counter[last_ch] += 1
        last_ch_idx = last_ch_counter[last_ch]
        record = BWTRecord(first_ch, first_ch_idx, last_ch, last_ch_idx)
        ret.append(record)
    for i, record_a in enumerate(ret):
        last = record_a.last_ch, record_a.last_ch_idx
        for j, record_b in enumerate(ret):
            first = record_b.first_ch, record_b.first_ch_idx
            if last == first:
                record_a.last_to_first_idx = j
                break
    return ret


def to_partial_suffix_array(
        seq: str,
        end_marker: str,
        k: int
) -> dict[int, int]:
    arr = SuffixArray.to_suffix_array(
        StringView.wrap(seq),
        StringView.wrap(end_marker)
    )
    return {i: sv.start for i, sv in enumerate(arr) if sv.start % k == 0}
# MARKDOWN_BUILD


# MARKDOWN_TEST
def walk_back_until_suffix_array_entry(
        bwt_array: list[BWTRecord],
        partial_suffix_array: dict[int, int],
        index: int
) -> int:
    walk_cnt = 0
    while index not in partial_suffix_array:
        index = bwt_array[index].last_to_first_idx
        walk_cnt += 1
    return partial_suffix_array[index] + walk_cnt


def find(
        bwt_array: list[BWTRecord],
        partial_suffix_array: dict[int, int],
        test: str
) -> list[int]:
    top = 0
    bottom = len(bwt_array) - 1
    for ch in reversed(test):
        new_top = len(bwt_array)
        new_bottom = -1
        for i in range(top, bottom + 1):
            record = bwt_array[i]
            if ch == record.last_ch:
                new_top = min(new_top, record.last_to_first_idx)
                new_bottom = max(new_bottom, record.last_to_first_idx)
        if new_bottom == -1 or new_top == len(bwt_array):  # technically only need to check one of these conditions
            return []
        top = new_top
        bottom = new_bottom
    positions = []
    for i in range(top, bottom + 1):
        pos = walk_back_until_suffix_array_entry(bwt_array, partial_suffix_array, i)
        positions.append(pos)
    return positions
# MARKDOWN_TEST


bwt_array = to_bwt(
    'panamabananas$',
    '$'
)
partial_suffix_array = to_partial_suffix_array(
    'panamabananas$',
    '$',
    5
)
for e in bwt_array:
    print(f'{e}')
print(f'{find(bwt_array, partial_suffix_array, "ana")}')
# print(f'{find(res, "fna")}')