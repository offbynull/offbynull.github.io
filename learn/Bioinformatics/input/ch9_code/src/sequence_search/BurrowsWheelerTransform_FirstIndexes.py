import functools
from collections import Counter
from sys import stdin

import yaml

from sequence_search.BurrowsWheelerTransform_Basic import cmp
from sequence_search.SearchUtils import RotatedListView


# MARKDOWN_BUILD
class BWTRecord:
    __slots__ = ['first_ch', 'first_ch_cnt', 'last_ch', 'last_ch_cnt', 'last_to_first_ptr', 'first_idx']

    def __init__(self, first_ch: str, first_ch_cnt: int, last_ch: str, last_ch_cnt: int, last_to_first_ptr: int, first_idx: int):
        self.first_ch = first_ch
        self.first_ch_cnt = first_ch_cnt
        self.last_ch = last_ch
        self.last_ch_cnt = last_ch_cnt
        self.last_to_first_ptr = last_to_first_ptr
        self.first_idx = first_idx


def to_bwt_with_first_indexes(
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
    seq_with_counts_rotations = [(i, RotatedListView(i, seq_with_counts)) for i in range(len(seq_with_counts))]  # rotations + new first_idx for each rotation
    seq_with_counts_rotations_sorted = sorted(
        seq_with_counts_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp(a[1], b[1], end_marker))
    )
    # Create BWT records
    bwt_records = []
    for first_idx, s in seq_with_counts_rotations_sorted:
        first_ch, first_ch_cnt = s[0]
        last_ch, last_ch_cnt = s[-1]
        last_to_first_ptr = next(i for i, (_, row) in enumerate(seq_with_counts_rotations_sorted) if s[-1] == row[0])
        record = BWTRecord(first_ch, first_ch_cnt, last_ch, last_ch_cnt, last_to_first_ptr, first_idx)
        bwt_records.append(record)
    return bwt_records
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
        bwt_records = to_bwt_with_first_indexes(seq, end_marker)
        print()
        print(f'The following first and last columns were produced ...')
        print()
        print(f' * First: {[r.first_ch + str(r.first_ch_cnt) for r in bwt_records]}')
        print(f' * First Indexes: {[r.first_idx for r in bwt_records]}')
        print(f' * Last: {[r.last_ch + str(r.last_ch_cnt) for r in bwt_records]}')
        print(f' * Last-to-First: {[r.last_to_first_ptr for r in bwt_records]}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")














# MARKDOWN_TEST
def walk_find(
        bwt_records: list[BWTRecord],
        test: str,
        start_row: int
) -> int | None:
    row = start_row
    for ch in reversed(test[:-1]):
        if bwt_records[row].last_ch != ch:
            return None
        row = bwt_records[row].last_to_first_ptr
    return bwt_records[row].first_idx


def find(
        bwt_records: list[BWTRecord],
        test: str
) -> list[int]:
    found = []
    for i, rec in enumerate(bwt_records):
        if rec.first_ch == test[-1]:
            if len(test) == 1:
                found.append(rec.first_idx)
            elif rec.last_ch == test[-2]:
                found_idx = walk_find(bwt_records, test, i)
                if found_idx is not None:
                    found.append(found_idx)
    return found
# MARKDOWN_TEST


def main_test():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        test = data['test']
        first = data['first']
        first_indexes = data['first_indexes']
        last = data['last']
        last_to_first = data['last_to_first']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records = []
        for (first_ch, first_ch_cnt), first_idx, (last_ch, last_ch_cnt), last_to_first_ptr in zip(first, first_indexes, last, last_to_first):
            bwt_records.append(BWTRecord(first_ch, first_ch_cnt, last_ch, last_ch_cnt, last_to_first_ptr, first_idx))
        found_indices = find(bwt_records, test)
        print()
        print(f'*{test}* found at indices {found_indices}.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")










if __name__ == '__main__':
    main_build()
