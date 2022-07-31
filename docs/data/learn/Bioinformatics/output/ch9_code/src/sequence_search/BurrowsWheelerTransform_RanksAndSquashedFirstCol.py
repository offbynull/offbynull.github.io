import functools
from bisect import bisect_left
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


def to_counts(
        bwt_array: list[BWTRecord]
) -> list[Counter[str]]:
    ret = [Counter()]
    for record in bwt_array:
        ch = record.last_ch
        counter = ret[-1].copy()
        counter[ch] += 1
        ret.append(counter)
    return ret
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
        bwt_counts: list[Counter],
        test: str
) -> int:
    top = 0
    bottom = len(bwt_array) - 1
    for ch in reversed(test):
        ch_top = bwt_counts[top][ch] + 1
        ch_bottom = bwt_counts[bottom + 1][ch]
        if ch_bottom < ch_top not in bwt_counts:
            return 0
        top = bwt_first_occurrence_map[ch] + ch_top - 1
        bottom = bwt_first_occurrence_map[ch] + ch_bottom - 1
    return (bottom - top) + 1
# MARKDOWN_TEST


bwt_array, bwt_first_occurrence_map = to_bwt_and_first_occurrences(
    'panamabananas$',
    '$'
)
bwt_counters = to_counts(bwt_array)
for e in bwt_array:
    print(f'{e}')
print(f'{find(bwt_array, bwt_first_occurrence_map, bwt_counters, "ana")}')
print(f'{find(bwt_array, bwt_first_occurrence_map, bwt_counters, "bna")}')