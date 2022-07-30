import functools
from bisect import bisect_left
from collections import Counter

from helpers.Utils import rotate_right
from sequence_search import SuffixArray
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
    raise '???'


class BWTRecord:
    __slots__ = ['last_ch', 'last_ch_idx']

    def __init__(self, last_ch: str, last_ch_idx: int):
        self.last_ch = last_ch
        self.last_ch_idx = last_ch_idx

    def __str__(self):
        return f'{self.last_ch}{self.last_ch_idx}'

    def __repr__(self):
        return str(self)


def to_bwt_and_first_occurrences(
        seq: str,
        end_marker: str
) -> tuple[list[BWTRecord], dict[str, int]]:
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
    last_first_ch = None
    last_ch_counter = Counter()
    bwt_array = []
    bwt_first_occurrence_map = {}
    for i, (s, idx) in enumerate(rotations_with_counts_sorted):
        first_ch = s[0]
        last_ch = s[-1]
        last_ch_counter[last_ch] += 1
        last_ch_idx = last_ch_counter[last_ch]
        bwt_record = BWTRecord(last_ch, last_ch_idx)
        bwt_array.append(bwt_record)
        if first_ch != last_first_ch:
            bwt_first_occurrence_map[first_ch] = i
            last_first_ch = first_ch
    return bwt_array, bwt_first_occurrence_map


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
def to_partial_counts(
        bwt_array: list[BWTRecord],
        n: int
) -> dict[int, Counter[str]]:
    counter = Counter()
    ret = {}
    for i, record in enumerate(bwt_array):
        if i % n == 0:
            ret[i] = counter.copy()
        counter[record.last_ch] += 1
    size = len(bwt_array)
    if size % n == 0:
        ret[size] = counter
    return ret


def walk_to_count(
        bwt_array: list[BWTRecord],
        bwt_array_idx: int,
        bwt_partial_counts: dict[int, Counter[str]],
        n: int
) -> Counter[str]:
    if bwt_array_idx in bwt_partial_counts:
        return bwt_partial_counts[bwt_array_idx]  # return as-is (no copying -- shouldn't get modified by called)
    offset = bwt_array_idx % n
    idx_start = bwt_array_idx - offset
    idx_end = min(bwt_array_idx, len(bwt_array) - 1)
    counter = bwt_partial_counts[idx_start].copy()  # copy it because it'll be modified
    record = bwt_array[idx_start]
    for i in range(idx_start + 1, idx_end + 1):
        counter[record.last_ch] += 1
        record = bwt_array[i]
    if bwt_array_idx == len(bwt_array):
        counter[record.last_ch] += 1
    return counter
# MARKDOWN_BUILD

# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.
# LOOK AT COUNT LOGIC AGAIN -- IN FAILURE CASES (WHERE STRING DOESNT EXIST), TOP WILL BE > BOTTOM.




# MARKDOWN_TEST
def walk_back_until_suffix_array_entries(
        bwt_array: list[BWTRecord],
        bwt_first_occurrence_map: dict[str, int],
        bwt_partial_counts: dict[int, Counter[str]],
        bwt_partial_counts_skip: int,
        partial_suffix_array: dict[int, int],
        bwt_top: int,
        bwt_bottom: int,
        walk_back_count: int = 0
) -> list[int]:
    walk_cnts = []
    for index in range(bwt_top, bwt_bottom + 1):
        cnts = get_suffix_array_entry_or_continue_walking_back(
            bwt_array,
            bwt_first_occurrence_map,
            bwt_partial_counts,
            bwt_partial_counts_skip,
            partial_suffix_array,
            index,
            bwt_top,
            bwt_bottom,
            walk_back_count
        )
        for cnt in cnts:
            walk_cnts.append(cnt)
    return walk_cnts


def get_suffix_array_entry_or_continue_walking_back(
        bwt_array: list[BWTRecord],
        bwt_first_occurrence_map: dict[str, int],
        bwt_partial_counts: dict[int, Counter[str]],
        bwt_partial_counts_skip: int,
        partial_suffix_array: dict[int, int],
        bwt_index: int,
        bwt_top: int,
        bwt_bottom: int,
        walk_back_count: int
) -> list[int]:
    if bwt_index in partial_suffix_array:
        seq_index = partial_suffix_array[bwt_index]
        return [seq_index + walk_back_count]
    next_ch = bwt_array[bwt_index].last_ch
    next_counter_top = walk_to_count(bwt_array, bwt_top, bwt_partial_counts, bwt_partial_counts_skip)
    next_ch_top = next_counter_top[next_ch] + 1
    next_counter_bottom = walk_to_count(bwt_array, bwt_bottom + 1, bwt_partial_counts, bwt_partial_counts_skip)
    next_ch_bottom = next_counter_bottom[next_ch]
    next_bwt_top = bwt_first_occurrence_map[next_ch] + next_ch_top - 1
    next_bwt_bottom = bwt_first_occurrence_map[next_ch] + next_ch_bottom - 1
    walk_cnts = walk_back_until_suffix_array_entries(
        bwt_array,
        bwt_first_occurrence_map,
        bwt_partial_counts,
        bwt_partial_counts_skip,
        partial_suffix_array,
        next_bwt_top,
        next_bwt_bottom,
        walk_back_count + 1
    )
    return walk_cnts


def find(
        bwt_array: list[BWTRecord],
        bwt_first_occurrence_map: dict[str, int],
        bwt_partial_counts: dict[int, Counter[str]],
        bwt_partial_counts_skip: int,
        partial_suffix_array: dict[int, int],
        test: str
) -> list[int]:
    top = 0
    bottom = len(bwt_array) - 1
    for ch in reversed(test):
        counter_top = walk_to_count(bwt_array, top, bwt_partial_counts, bwt_partial_counts_skip)
        ch_top = counter_top[ch] + 1
        counter_bottom = walk_to_count(bwt_array, bottom + 1, bwt_partial_counts, bwt_partial_counts_skip)
        ch_bottom = counter_bottom[ch]
        if ch_bottom < ch_top not in bwt_partial_counts:
            return []
        top = bwt_first_occurrence_map[ch] + ch_top - 1
        bottom = bwt_first_occurrence_map[ch] + ch_bottom - 1
    positions = walk_back_until_suffix_array_entries(
        bwt_array,
        bwt_first_occurrence_map,
        bwt_partial_counts,
        bwt_partial_counts_skip,
        partial_suffix_array,
        top,
        bottom
    )
    return positions
# MARKDOWN_TEST


bwt_array, bwt_first_occurrence_map = to_bwt_and_first_occurrences(
    'panamabananas$',
    '$'
)
bwt_partial_counts = to_partial_counts(bwt_array, 5)
partial_suffix_array = to_partial_suffix_array(
    'panamabananas$',
    '$',
    5
)
for i in range(len(bwt_array) + 1):
    print(f'{walk_to_count(bwt_array, i, bwt_partial_counts, 5)}')
for e in bwt_array:
    print(f'{e}')
print(f'{find(bwt_array, bwt_first_occurrence_map, bwt_partial_counts, 5, partial_suffix_array, "ana")}')
print(f'{find(bwt_array, bwt_first_occurrence_map, bwt_partial_counts, 5, partial_suffix_array, "bna")}')