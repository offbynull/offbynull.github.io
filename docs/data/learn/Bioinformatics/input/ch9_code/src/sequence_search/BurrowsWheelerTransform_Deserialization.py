import functools
from bisect import bisect_left
from collections import Counter
from sys import stdin

import yaml

from sequence_search.BurrowsWheelerTransform_Basic_LastToFirst import BWTRecord, walk
from sequence_search.SearchUtils import RotatedStringView





# We need to go through all this wrpaping because bisect_left won't let you submit a key parameter that produces a type
# different than the type in the collection, which means functools.cmp_to_key() doesn't work with bisect left.
class FirstColBisectableWrapper:
    def __init__(self, first, end_marker):
        self.it = first
        self.end_marker = end_marker

    def __getitem__(self, i):
        return FirstColBisectableWrapper.KeyWrapper(self.it[i], self.end_marker)

    def __len__(self):
        return len(self.it)

    class KeyWrapper:
        def __init__(self, v: tuple[str, int], end_marker: str):
            self.v = v
            self.end_marker = end_marker

        def __lt__(self, other: tuple[str, int]):
            if cmp_symbol_and_count(self.v, other, self.end_marker) < 0:
                return True
            else:
                return False






# MARKDOWN_DESERIALIZE
def cmp_symbol(a: str, b: str, end_marker: str):
    if len(a) != len(b):
        raise '???'
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
    return 0


def cmp_symbol_and_count(a: tuple[str, int], b: tuple[str, int], end_marker: str):
    # compare symbol
    x = cmp_symbol(a[0], b[0], end_marker)
    if x != 0:
        return x
    # compare symbol instance count
    if a[1] < b[1]:
        return -1
    elif a[1] > b[1]:
        return 1
    return 0


def to_bwt_from_last_sequence(
        last_seq: str,
        end_marker: str
) -> list[BWTRecord]:
    # Create first and last columns
    bwt_records = []
    last_ch_counter = Counter()
    last = []
    for last_ch in last_seq:
        last_ch_counter[last_ch] += 1
        last_ch_count = last_ch_counter[last_ch]
        last.append((last_ch, last_ch_count))
    first = sorted(last, key=functools.cmp_to_key(lambda a, b: cmp_symbol_and_count(a, b, end_marker)))
    for (first_ch, first_ch_cnt), (last_ch, last_ch_cnt) in zip(first, last):
        # Create record
        rec = BWTRecord(first_ch, first_ch_cnt, last_ch, last_ch_cnt, -1)
        # Figure out where in first that (last_ch, last_ch_cnt) occurs using binary search. This is
        # possible because first is sorted.
        rec.last_to_first_ptr = bisect_left(
            FirstColBisectableWrapper(first, end_marker),
            (last_ch, last_ch_cnt)
        )
        # Append to return
        bwt_records.append(rec)
    return bwt_records
# MARKDOWN_DESERIALIZE


def main_deserialize():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        last_seq = data['last_seq']
        end_marker = data['end_marker']
        print(f'Deserializing BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records = to_bwt_from_last_sequence(last_seq, end_marker)
        print()
        print(f'The following first and last columns were produced ...')
        print()
        print(f' * First: {[(r.first_ch, r.first_ch_cnt) for r in bwt_records]}')
        print(f' * Last: {[(r.last_ch, r.last_ch_cnt) for r in bwt_records]}')
        print(f' * Last-to-First: {[r.last_to_first_ptr for r in bwt_records]}')
        print()
        seq = walk(bwt_records)
        print()
        print(f'The original sequence reconstructed from the BWT array: *{seq}*.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")















# MARKDOWN_OPTIMIZED_BUILD
def to_bwt_optimized(
        seq: str,
        end_marker: str
) -> list[BWTRecord]:
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    seq_rotations = [RotatedStringView(i, seq) for i in range(len(seq))]
    seq_rotations_sorted = sorted(
        seq_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp_symbol(a, b, end_marker))
    )
    last_seq = ''.join(row[-1] for row in seq_rotations_sorted)
    return to_bwt_from_last_sequence(last_seq, end_marker)
# MARKDOWN_OPTIMIZED_BUILD


def main_optimized_build():
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
        bwt_records = to_bwt_optimized(seq, end_marker)
        print()
        print(f'The following first and last columns were produced ...')
        print()
        print(f' * First: {[(r.first_ch, r.first_ch_cnt) for r in bwt_records]}')
        print(f' * Last: {[(r.last_ch, r.last_ch_cnt) for r in bwt_records]}')
        print(f' * Last-to-First: {[r.last_to_first_ptr for r in bwt_records]}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")
























# MARKDOWN_OPTIMIZED2_BUILD
def to_bwt_optimized2(
        seq: str,
        end_marker: str
) -> list[BWTRecord]:
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    # Create first and last columns
    seq_rotations = [RotatedStringView(i, seq) for i in range(len(seq))]
    seq_rotations_sorted = sorted(
        seq_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp_symbol(a, b, end_marker))
    )
    first_ch_counter = Counter()
    last_ch_counter = Counter()
    first = []
    last = []
    bwt_records = []
    for i, s in enumerate(seq_rotations_sorted):
        first_ch = s[0]
        first_ch_counter[first_ch] += 1
        first_ch_cnt = first_ch_counter[first_ch]
        last_ch = s[-1]
        last_ch_counter[last_ch] += 1
        last_ch_cnt = last_ch_counter[last_ch]
        first.append((first_ch, first_ch_cnt))
        last.append((last_ch, last_ch_cnt))
    for (first_ch, first_ch_cnt), (last_ch, last_ch_cnt) in zip(first, last):
        # Create record
        rec = BWTRecord(first_ch, first_ch_cnt, last_ch, last_ch_cnt, -1)
        # Figure out where in first that (last_ch, last_ch_cnt) occurs using binary search. This is
        # possible because first is sorted.
        rec.last_to_first_ptr = bisect_left(
            FirstColBisectableWrapper(first, end_marker),
            (last_ch, last_ch_cnt)
        )
        # Append to return
        bwt_records.append(rec)
    return bwt_records
# MARKDOWN_OPTIMIZED2_BUILD


def main_optimized2_build():
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
        bwt_records = to_bwt_optimized2(seq, end_marker)
        print()
        print(f'The following first and last columns were produced ...')
        print()
        print(f' * First: {[(r.first_ch, r.first_ch_cnt) for r in bwt_records]}')
        print(f' * Last: {[(r.last_ch, r.last_ch_cnt) for r in bwt_records]}')
        print(f' * Last-to-First: {[r.last_to_first_ptr for r in bwt_records]}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")









if __name__ == '__main__':
    main_optimized_build()
