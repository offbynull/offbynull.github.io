import functools
from bisect import bisect_right, bisect_left
from collections import Counter, defaultdict

from helpers.Utils import rotate_right
from sequence_search.SearchUtils import StringView


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


class BisectCompatibleBWTComparison(object):
    __slots__ = ['obj', 'end_marker']

    def __init__(self, obj: str, end_marker: str):
        self.obj = obj
        self.end_marker = end_marker

    def __lt__(self, other):
        return self.end_marker == other.end_marker and cmp(self.obj, other.obj, self.end_marker) < 0


# MARKDOWN
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
            first_ch_idx = first_ch_counter[first_ch]
            first_ch_counter[first_ch] += 1
            last_ch = s[-1]
            last_ch_idx = last_ch_counter[last_ch]
            last_ch_counter[last_ch] += 1
            if first_ch != old_first_ch:
                self.first_chs.append(first_ch)
                old_first_ch = first_ch
            self.first_ch_to_last_ch_mapping[first_ch].append((last_ch, last_ch_idx))

    def max_bounds(self):
        top_ch = self.first_chs[0]
        top = (top_ch, 0)
        bottom_ch = self.first_chs[-1]
        bottom = (bottom_ch, len(self.first_ch_to_last_ch_mapping[bottom_ch]) - 1)
        return top, bottom

    def binary_search_first_ch_array(
            self,
            top_first_ch: str,
            bottom_first_ch: str
    ):
        # binary search to idx of top first_ch
        top_idx = bisect_left(
            self.first_chs,
            BisectCompatibleBWTComparison(top_first_ch, self.end_marker),
            key=lambda x: BisectCompatibleBWTComparison(x, self.end_marker)
        )
        if self.first_chs[top_idx] != top_first_ch:
            return None
        # binary search to idx of bottom first_ch
        bottom_idx = bisect_left(
            self.first_chs,
            BisectCompatibleBWTComparison(bottom_first_ch, self.end_marker),
            lo=top_idx,
            key=lambda x: BisectCompatibleBWTComparison(x, self.end_marker)
        )
        if self.first_chs[bottom_idx] != bottom_first_ch:
            return None
        return top_idx, bottom_idx

    def last_to_first(
            self,
            top_bound: tuple[str, int],
            bottom_bound: tuple[str, int],
            ch: str
    ):
        top_first_ch, top_first_ch_idx = top_bound
        bottom_first_ch, bottom_first_ch_idx = bottom_bound
        # binary search to idx of top first_ch and bottom_first_ch (which should be after top)
        search_res = self.binary_search_first_ch_array(top_first_ch, bottom_first_ch)
        if search_res is None:
            return None
        top_idx, bottom_idx = search_res
        # setup scan vars
        new_top = None
        new_bottom = None
        # scan top (possibly a partial scan -- maybe starting somewhere in the middle)
        top_mappings = self.first_ch_to_last_ch_mapping[top_first_ch]
        for first_ch_idx in range(top_first_ch_idx, len(top_mappings)):
            last_ch, last_ch_idx = top_mappings[first_ch_idx]
            if ch == last_ch:
                bound = last_ch, last_ch_idx
                new_top = bound if new_top is None else min(new_top, bound)
                new_bottom = bound if new_bottom is None else max(new_bottom, bound)
        # scan inbetween
        for i in range(top_idx + 1, bottom_idx):
            first_ch = self.first_chs[i]
            for first_ch_idx, (last_ch, last_ch_idx) in enumerate(self.first_ch_to_last_ch_mapping[first_ch]):
                if ch == last_ch:
                    bound = last_ch, last_ch_idx
                    new_top = bound if new_top is None else min(new_top, bound)
                    new_bottom = bound if new_bottom is None else max(new_bottom, bound)
        # scan bottom (possibly a partial scan -- maybe stopping before the end)
        bottom_mappings = self.first_ch_to_last_ch_mapping[bottom_first_ch]
        for first_ch_idx in range(0, bottom_first_ch_idx + 1):
            last_ch, last_ch_idx = bottom_mappings[first_ch_idx]
            if ch == last_ch:
                bound = last_ch, last_ch_idx
                new_top = bound if new_top is None else min(new_top, bound)
                new_bottom = bound if new_bottom is None else max(new_bottom, bound)
        # return
        return new_top, new_bottom

    def find(self, test: str) -> int:
        top, bottom = self.max_bounds()
        for ch in reversed(test):
            res = self.last_to_first(top, bottom, ch)
            if res is None:
                return 0
            top, bottom = res
        # count number of hops
        top_first_ch, top_first_ch_idx = top
        bottom_first_ch, bottom_first_ch_idx = bottom
        assert top_first_ch == bottom_first_ch
        return bottom_first_ch_idx - top_first_ch_idx + 1
# MARKDOWN


res = BWTArray(
    'panamabananas$',
    '$'
)
top, bottom = res.max_bounds()
res.last_to_first(top, bottom, 'a')
print(f'{res.find("ana")}')