import functools
from bisect import bisect_left, bisect_right
from collections import Counter
from sys import stdin
from typing import Any

import yaml

from helpers.Utils import rotate_right


# MARKDOWN_BUILD
def cmp(a: list[tuple[str, int]], b: list[tuple[str, int]], end_marker: str):
    if len(a) != len(b):
        raise '???'
    for (a_ch, _), (b_ch, _) in zip(a, b):
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
    return 0


class BWTRecord:
    __slots__ = ['first_ch', 'first_ch_cnt', 'last_ch', 'last_ch_cnt', 'last_to_first_idx']

    def __init__(self, first_ch: str, first_ch_cnt: int, last_ch: str, last_ch_cnt: int):
        self.first_ch = first_ch
        self.first_ch_cnt = first_ch_cnt
        self.last_ch = last_ch
        self.last_ch_cnt = last_ch_cnt
        self.last_to_first_idx = -1


def to_bwt(
        seq: str,
        end_marker: str
) -> list[BWTRecord]:
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    # Create matrix
    seq_with_counts = []
    seq_ch_counter = Counter()
    for ch in seq:
        seq_ch_counter[ch] += 1
        ch_cnt = seq_ch_counter[ch]
        seq_with_counts.append((ch, ch_cnt))
    seq_with_counts_rotations = rotate_right(seq_with_counts)
    seq_with_counts_rotations_sorted = sorted(
        seq_with_counts_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp(a, b, end_marker))
    )
    # Pull out first and last columns
    ret = []
    for s in seq_with_counts_rotations_sorted:
        first_ch, first_ch_cnt = s[0]
        last_ch, last_ch_cnt = s[-1]
        record = BWTRecord(first_ch, first_ch_cnt, last_ch, last_ch_cnt)
        ret.append(record)
    # Populate record last-to-first pointers
    for i, record_a in enumerate(ret):
        last = record_a.last_ch, record_a.last_ch_cnt
        for j, record_b in enumerate(ret):
            first = record_b.first_ch, record_b.first_ch_cnt
            if last == first:
                record_a.last_to_first_idx = j
                break
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
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records = to_bwt(seq, end_marker)
        print()
        print(f'The following first and last columns were produced ...')
        print()
        print(f' * First: {[r.first_ch + str(r.first_ch_cnt) for r in bwt_records]}')
        print(f' * Last: {[r.last_ch + str(r.last_ch_cnt) for r in bwt_records]}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")














def to_bwt_from_first_last_cols(
        first_col: list[list[Any]],
        last_col: list[list[Any]]
) -> list[BWTRecord]:
    ret = []
    for first, last in zip(first_col, last_col):
        record = BWTRecord(first[0], first[1], last[0], last[1])
        ret.append(record)
    for i, record_a in enumerate(ret):
        last = record_a.last_ch, record_a.last_ch_cnt
        for j, record_b in enumerate(ret):
            first = record_b.first_ch, record_b.first_ch_cnt
            if last == first:
                record_a.last_to_first_idx = j
                break
    return ret


# MARKDOWN_WALK
def walk(bwt_records: list[BWTRecord]) -> str:
    ret = ''
    row = 0  # first idx of bwt_records always has first_ch == end_marker because of the lexicographical sorting
    while True:
        ret += bwt_records[row].last_ch
        row = bwt_records[row].last_to_first_idx
        if row == 0:
            break
    ret = ret[::-1]  # reverse ret
    ret = ret[1:] + ret[0]  # ret has end_marker at beginning, rotate it to end
    return ret
# MARKDOWN_WALK


def main_walk():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        first_col = data['first_col']
        last_col = data['last_col']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records = to_bwt_from_first_last_cols(first_col, last_col)
        seq = walk(bwt_records)
        print()
        print(f'The original sequence was *{seq}*.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")














# MARKDOWN_TEST
def walk_find(
        bwt_records: list[BWTRecord],
        test: str,
        start_row: int
) -> bool:
    row = start_row
    for ch in reversed(test[:-1]):
        if bwt_records[row].last_ch != ch:
            return False
        row = bwt_records[row].last_to_first_idx
    return True


def find(
        bwt_records: list[BWTRecord],
        test: str
) -> int:
    found = 0
    for i, rec in enumerate(bwt_records):
        if rec.first_ch == test[-1]:
            if len(test) == 1 or (rec.last_ch == test[-2] and walk_find(bwt_records, test, i)):
                found += 1
    return found
    # The code above is the obvious way to do this. However, since the first column is always sorted by character, the
    # entire array doesn't need to be scanned. Instead, you can binary search to the first and last index with
    # rec.first_ch == test[-1] and just consider those indices.
    #
    # The problem with doing this is that bisect_left/bisect_right has a requirement where the binary array being
    # searched must contain the same type as the element being searched for. Even with a custom sorting "key" to try to
    # map between the types on comparison, it won't allow it. Otherwise, the code below would probably work fine...
    #
    # end_marker = bwt_records[0].first_ch  # bwt_records[0] always has first_ch == end_marker because of lexicographic sort
    # found = 0
    # # Binary search the bwt_records for the left-most (top) entry with first_ch in its
    # bwt_top = bisect_left(
    #     bwt_records,
    #     test[-1],
    #     key=functools.cmp_to_key(lambda a, b: cmp(a.first_ch[0], b.first_ch[0], end_marker)))
    # if bwt_top == len(test):
    #     return 0  # not found
    # # Binary search the bwt_records for the right-most (bottom) entry with first_ch in its
    # bwt_bottom = bisect_right(
    #     bwt_records,
    #     test[-1],
    #     lo=bwt_top,
    #     key=functools.cmp_to_key(lambda a, b: cmp(a.first_ch[0], b.first_ch[0], end_marker)))
    # # If you're only searching for a single character, stop here.
    # if len(test) == 1:
    #     return bwt_bottom - bwt_top + 1
    # # Otherwise, scan only between those indices
    # for i in range(bwt_top, bwt_bottom + 1):
    #     rec = bwt_records[i]
    #     if rec.last_ch == test[-2] and walk_find(bwt_records, test, i):
    #         found += 1
    # return found
# MARKDOWN_TEST


def main_test():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        test = data['test']
        seq = data['sequence']
        end_marker = data['end_marker']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records = to_bwt(seq, end_marker)
        print()
        print(f'The following first and last columns were produced ...')
        print()
        print(f' * First: {[r.first_ch + str(r.first_ch_cnt) for r in bwt_records]}')
        print(f' * Last: {[r.last_ch + str(r.last_ch_cnt) for r in bwt_records]}')
        print()
        found_cnt = find(bwt_records, test)
        print()
        print(f'*{test}* found in *{seq}* at {found_cnt} times.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")










if __name__ == '__main__':
    main_test()
