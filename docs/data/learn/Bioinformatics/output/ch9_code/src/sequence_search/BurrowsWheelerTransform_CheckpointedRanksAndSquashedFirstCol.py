import functools
from collections import Counter

from helpers.Utils import rotate_right
from sequence_search.BurrowsWheelerTransform_Deserialization import cmp_char_only


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
    # Create first and last columns
    seq_rotations = rotate_right(seq)
    seq_rotations_sorted = sorted(
        seq_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp_char_only(a, b, end_marker))
    )
    last_first_ch = None
    last_ch_counter = Counter()
    bwt_array = []
    bwt_first_occurrence_map = {}
    for i, s in enumerate(seq_rotations_sorted):
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
def find(
        bwt_array: list[BWTRecord],
        bwt_first_occurrence_map: dict[str, int],
        bwt_partial_counts: dict[int, Counter[str]],
        n: int,
        test: str
) -> int:
    top = 0
    bottom = len(bwt_array) - 1
    for ch in reversed(test):
        counter_top = walk_to_count(bwt_array, top, bwt_partial_counts, n)
        ch_top = counter_top[ch] + 1
        counter_bottom = walk_to_count(bwt_array, bottom + 1, bwt_partial_counts, n)
        ch_bottom = counter_bottom[ch]
        if ch_bottom < ch_top not in bwt_partial_counts:
            return 0
        top = bwt_first_occurrence_map[ch] + ch_top - 1
        bottom = bwt_first_occurrence_map[ch] + ch_bottom - 1
    return (bottom - top) + 1
# MARKDOWN_TEST


bwt_array, bwt_first_occurrence_map = to_bwt_and_first_occurrences(
    'panamabananas$',
    '$'
)
bwt_partial_counts = to_partial_counts(bwt_array, 5)
for i in range(len(bwt_array) + 1):
    print(f'{walk_to_count(bwt_array, i, bwt_partial_counts, 5)}')
for e in bwt_array:
    print(f'{e}')
print(f'{find(bwt_array, bwt_first_occurrence_map, bwt_partial_counts, 5, "ana")}')
print(f'{find(bwt_array, bwt_first_occurrence_map, bwt_partial_counts, 5, "bna")}')