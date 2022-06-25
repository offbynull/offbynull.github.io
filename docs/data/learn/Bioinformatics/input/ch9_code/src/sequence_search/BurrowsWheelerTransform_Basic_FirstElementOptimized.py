import functools
from bisect import bisect_right, bisect_left
from collections import Counter, defaultdict

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
    return 0

class BWTComparableStr(object):
    __slots__ = ['obj', 'end_marker']

    def __init__(self, obj: str, end_marker: str):
        self.obj = obj
        self.end_marker = end_marker

    def __lt__(self, other):
        return self.end_marker == other.end_marker and cmp(self.obj, other.obj, self.end_marker) < 0


class BWTRecord:
    __slots__ = ['first_ch', 'first_ch_idx', 'last_ch', 'last_ch_idx']

    def __init__(self, first_ch: str, first_ch_idx: int, last_ch: str, last_ch_idx: int):
        self.first_ch = first_ch
        self.first_ch_idx = first_ch_idx
        self.last_ch = last_ch
        self.last_ch_idx = last_ch_idx

    def __str__(self):
        return str((self.first_ch + str(self.first_ch_idx), self.last_ch + str(self.last_ch_idx)))

    def __repr__(self):
        return str(self)


class BWTArray:
    def __init__(self, seq: str, end_marker: str):
        assert end_marker == seq[-1], f'{seq} missing end marker'
        assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
        self.end_marker = end_marker
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
        old_first_ch = None
        self.first_chs = []
        self.first_ch_to_last_ch_mapping = defaultdict(list)
        for i, (s, idx) in enumerate(rotations_with_counts_sorted):
            first_ch = s[0]
            first_ch_counter[first_ch] += 1
            first_ch_idx = first_ch_counter[first_ch]
            last_ch = s[-1]
            last_ch_counter[last_ch] += 1
            last_ch_idx = last_ch_counter[last_ch]
            if first_ch != old_first_ch:
                self.first_chs.append(first_ch)
                old_first_ch = first_ch
            self.first_ch_to_last_ch_mapping[first_ch].append((last_ch, last_ch_idx))

    def bounds(self):
        top_ch = self.first_chs[0]
        top = (top_ch, 0)
        bottom_ch = self.first_chs[-1]
        bottom = (bottom_ch, len(self.first_ch_to_last_ch_mapping[bottom_ch]) - 1)
        return top, bottom

    def last_to_first(
            self,
            top_bound: tuple[str, int],
            bottom_bound: tuple[str, int],
            ch: str
    ):
        # binary search to idx of top first_ch
        top_first_ch, top_first_ch_idx = top_bound
        top_idx = bisect_left(
            self.first_chs,
            BWTComparableStr(top_first_ch, self.end_marker),
            key=lambda x: BWTComparableStr(x, self.end_marker)
        )
        if self.first_chs[top_idx] != top_first_ch:
            return None
        # binary search to idx of bottom first_ch
        bottom_first_ch, bottom_first_ch_idx = bottom_bound
        bottom_idx = bisect_left(
            self.first_chs,
            BWTComparableStr(bottom_first_ch, self.end_marker),
            lo=top_idx,
            key=lambda x: BWTComparableStr(x, self.end_marker)
        )
        if self.first_chs[bottom_idx] != bottom_first_ch:
            return None
        # setup scan vars
        new_top = None
        new_bottom = None
        # scan first (last n)
        for first_ch_idx, (last_ch, last_ch_idx) in enumerate(self.first_ch_to_last_ch_mapping[top_first_ch]):
            if ch == last_ch:
                bound = top_first_ch, first_ch_idx
                new_top = bound if new_top is None else min(new_top, bound)
                new_bottom = bound if new_bottom is None else min(new_bottom, bound)
        # scan inbetween
        for i in range(top_idx + 1, bottom_idx):
            first_ch = self.first_chs[i]
            for first_ch_idx, (last_ch, last_ch_idx) in enumerate(self.first_ch_to_last_ch_mapping[first_ch]):
                if ch == last_ch:
                    bound = first_ch, first_ch_idx
                    new_top = bound if new_top is None else min(new_top, bound)
                    new_bottom = bound if new_bottom is None else min(new_bottom, bound)
        # scan bottom (first m)
        for first_ch_idx, (last_ch, last_ch_idx) in enumerate(self.first_ch_to_last_ch_mapping[bottom_first_ch]):
            if ch == last_ch:
                bound = bottom_first_ch, bottom_first_ch_idx
                new_top = bound if new_top is None else min(new_top, bound)
                new_bottom = bound if new_bottom is None else min(new_bottom, bound)
        return new_top, new_bottom

    WALK THE ABOVE 3 SCANS TO ENSURE THIS WORKS
    WALK THE ABOVE 3 SCANS TO ENSURE THIS WORKS
    WALK THE ABOVE 3 SCANS TO ENSURE THIS WORKS
    WALK THE ABOVE 3 SCANS TO ENSURE THIS WORKS
    WALK THE ABOVE 3 SCANS TO ENSURE THIS WORKS
    WALK THE ABOVE 3 SCANS TO ENSURE THIS WORKS
    WALK THE ABOVE 3 SCANS TO ENSURE THIS WORKS
    WALK THE ABOVE 3 SCANS TO ENSURE THIS WORKS
    WALK THE ABOVE 3 SCANS TO ENSURE THIS WORKS
    WALK THE ABOVE 3 SCANS TO ENSURE THIS WORKS
    WALK THE ABOVE 3 SCANS TO ENSURE THIS WORKS


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
# MARKDOWN_BUILD


# MARKDOWN_TEST
def find(
        bwt_array: list[BWTRecord],
        test: str
) -> int:
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
            return 0
        top = new_top
        bottom = new_bottom
    return (bottom - top) + 1
# MARKDOWN_TEST


res = BWTArray(
    'panamabananas$',
    '$'
)
top, bottom = res.bounds()
res.last_to_first(top, bottom, 'a')
for e in res:
    print(f'{e}')
print(f'{find(res, "ana")}')
# print(f'{find(res, "fna")}')