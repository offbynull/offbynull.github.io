import functools
from collections import Counter
from sys import stdin
from typing import Any

import yaml

from helpers.Utils import rotate_right_with_shift_counts
from sequence_search.BurrowsWheelerTransform_Basic import cmp


# MARKDOWN_BUILD
class BWTRecord:
    __slots__ = ['first_ch', 'first_ch_cnt', 'last_ch', 'last_ch_cnt', 'last_to_first_idx']

    def __init__(self, first_ch: str, first_ch_cnt: int, last_ch: str, last_ch_cnt: int):
        self.first_ch = first_ch
        self.first_ch_cnt = first_ch_cnt
        self.last_ch = last_ch
        self.last_ch_cnt = last_ch_cnt
        self.last_to_first_idx = -1


def to_bwt_with_first_indexes_checkpointed(
        seq: str,
        end_marker: str,
        first_indexes_checkpoint_n: int
) -> tuple[list[BWTRecord], dict[int, int]]:
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    # Create matrix
    seq_with_counts = []
    seq_ch_counter = Counter()
    for ch in seq:
        seq_ch_counter[ch] += 1
        ch_cnt = seq_ch_counter[ch]
        seq_with_counts.append((ch, ch_cnt))
    seq_with_counts_rotations = rotate_right_with_shift_counts(seq_with_counts)  # rotations + new first_idx for each rotation
    seq_with_counts_rotations_sorted = sorted(
        seq_with_counts_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp(a[1], b[1], end_marker))
    )
    # Pull out first and last columns
    bwt_records = []
    bwt_first_indexes_checkpoints = {}
    for i, (first_idx, s) in enumerate(seq_with_counts_rotations_sorted):
        first_ch, first_ch_cnt = s[0]
        last_ch, last_ch_cnt = s[-1]
        record = BWTRecord(first_ch, first_ch_cnt, last_ch, last_ch_cnt)
        bwt_records.append(record)
        if first_idx % first_indexes_checkpoint_n == 0:
            bwt_first_indexes_checkpoints[i] = first_idx
    # Populate record last-to-first pointers
    for i, record_a in enumerate(bwt_records):
        last = record_a.last_ch, record_a.last_ch_cnt
        for j, record_b in enumerate(bwt_records):
            first = record_b.first_ch, record_b.first_ch_cnt
            if last == first:
                record_a.last_to_first_idx = j
                break
    return bwt_records, bwt_first_indexes_checkpoints
# MARKDOWN_BUILD


def main_build():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        seq = data['sequence']
        end_marker = data['end_marker']
        first_indexes_checkpoint_n = data['first_indexes_checkpoint_n']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records, bwt_first_indexes_checkpoints = to_bwt_with_first_indexes_checkpointed(seq, end_marker, first_indexes_checkpoint_n)
        print()
        print(f'The following first and last columns were produced ...')
        print()
        print(f' * First: {[r.first_ch + str(r.first_ch_cnt) for r in bwt_records]}')
        print(f' * First Index Checkpoints: {bwt_first_indexes_checkpoints}')
        print(f' * Last: {[r.last_ch + str(r.last_ch_cnt) for r in bwt_records]}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")










# MARKDOWN_WALK_BACK_TO_FIRST_IDX
def walk_back_until_first_index_checkpoint(
        bwt_records: list[BWTRecord],
        bwt_first_indexes_checkpoints: dict[int, int],
        index: int
) -> int:
    walk_cnt = 0
    while index not in bwt_first_indexes_checkpoints:
        index = bwt_records[index].last_to_first_idx
        walk_cnt += 1
    first_idx = bwt_first_indexes_checkpoints[index] + walk_cnt
    # It's possible that the walk back continues backward before the start of the sequence, resulting
    # in it looping to the end and continuing to walk back from there. If that happens, the code below
    # adjusts it.
    sequence_len = len(bwt_records)
    if first_idx >= sequence_len:
        first_idx -= sequence_len
    return first_idx
# MARKDOWN_WALK_BACK_TO_FIRST_IDX


def main_walk_back_until_first_index_checkpoint():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        seq = data['sequence']
        end_marker = data['end_marker']
        first_indexes_checkpoint_n = data['first_indexes_checkpoint_n']
        from_index = data['from_index']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records, bwt_first_indexes_checkpoints = to_bwt_with_first_indexes_checkpointed(seq, end_marker, first_indexes_checkpoint_n)
        print()
        print(f'The following first and last columns were produced ...')
        print()
        print(f' * First: {[r.first_ch + str(r.first_ch_cnt) for r in bwt_records]}')
        print(f' * First Index Checkpoints: {bwt_first_indexes_checkpoints}')
        print(f' * Last: {[r.last_ch + str(r.last_ch_cnt) for r in bwt_records]}')
        print()
        first_idx = walk_back_until_first_index_checkpoint(bwt_records, bwt_first_indexes_checkpoints, from_index)
        print(f'Walking back to a first index checkpoint resulted in a first index of {first_idx} ...')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")












# MARKDOWN_TEST
def walk_find(
        bwt_records: list[BWTRecord],
        bwt_first_indexes_checkpoints: dict[int, int],
        test: str,
        start_row: int
) -> int | None:
    row = start_row
    for ch in reversed(test[:-1]):
        if bwt_records[row].last_ch != ch:
            return None
        row = bwt_records[row].last_to_first_idx
    first_idx = walk_back_until_first_index_checkpoint(bwt_records, bwt_first_indexes_checkpoints, row)
    return first_idx


def find(
        bwt_records: list[BWTRecord],
        bwt_first_indexes_checkpoints: dict[int, int],
        test: str
) -> list[int]:
    found = []
    for i, rec in enumerate(bwt_records):
        if rec.first_ch == test[-1]:
            if len(test) == 1:
                first_idx = walk_back_until_first_index_checkpoint(bwt_records, bwt_first_indexes_checkpoints, i)
                found.append(first_idx)
            elif rec.last_ch == test[-2]:
                found_idx = walk_find(bwt_records, bwt_first_indexes_checkpoints, test, i)
                if found_idx is not None:
                    found.append(found_idx)
    return found
    # The code above is the obvious way to do this. However, since the first column is always sorted by character, the
    # entire array doesn't need to be scanned. Instead, you can binary search to the first and last index with
    # rec.first_ch == test[-1] and just consider those indices.
    #
    # The problem with doing this is that bisect_left/bisect_right has a requirement where the binary array being
    # searched must contain the same type as the element being searched for. Even with a custom sorting "key" to try to
    # map between the types on comparison, it won't allow it. See the "standard algorithm" implementation for more info.
# MARKDOWN_TEST


def main_test():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        seq = data['sequence']
        end_marker = data['end_marker']
        first_indexes_checkpoint_n = data['first_indexes_checkpoint_n']
        test = data['test']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records, bwt_first_indexes_checkpoints = to_bwt_with_first_indexes_checkpointed(seq, end_marker, first_indexes_checkpoint_n)
        print()
        print(f'The following first and last columns were produced ...')
        print()
        print(f' * First: {[r.first_ch + str(r.first_ch_cnt) for r in bwt_records]}')
        print(f' * First Index Checkpoints: {bwt_first_indexes_checkpoints}')
        print(f' * Last: {[r.last_ch + str(r.last_ch_cnt) for r in bwt_records]}')
        print()
        found_indices = find(bwt_records, bwt_first_indexes_checkpoints, test)
        print()
        print(f'*{test}* found in *{seq}* at indices {found_indices}.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")










if __name__ == '__main__':
    main_test()
