import functools
from bisect import bisect_left, bisect_right
from collections import Counter
from sys import stdin
from typing import Any

import yaml

from helpers.Utils import rotate_right


# MARKDOWN_DESERIALIZE
from sequence_search.BurrowsWheelerTransform_Basic import BWTRecord, walk


def cmp_char_only(a: str, b: str, end_marker: str):
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


def cmp_char_and_instance(a: tuple[str, int], b: tuple[str, int], end_marker: str):
    # compare symbol
    x = cmp_char_only(a[0], b[0], end_marker)
    if x != 0:
        return x
    # compare symbol instance count
    if a[1] < b[1]:
        return -1
    elif a[1] > b[1]:
        return 1
    return 0


def to_bwt_from_last_sequence(
        last_col_seq: str,
        end_marker: str
) -> list[BWTRecord]:
    # Create first and last columns
    ret = []
    last_ch_counter = Counter()
    last_col = []
    for last_ch in last_col_seq:
        last_ch_counter[last_ch] += 1
        last_ch_count = last_ch_counter[last_ch]
        last_col.append((last_ch, last_ch_count))
    first_col = sorted(last_col, key=functools.cmp_to_key(lambda a, b: cmp_char_and_instance(a, b, end_marker)))
    for (first_ch, first_ch_idx), (last_ch, last_ch_idx) in zip(first_col, last_col):
        record = BWTRecord(first_ch, first_ch_idx, last_ch, last_ch_idx)
        ret.append(record)
    # Populate record last-to-first pointers
    for i, record_a in enumerate(ret):
        last = record_a.last_ch, record_a.last_ch_idx
        for j, record_b in enumerate(ret):
            first = record_b.first_ch, record_b.first_ch_idx
            if last == first:
                record_a.last_to_first_idx = j
                break
    return ret
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
        print(f' * First: {[r.first_ch + str(r.first_ch_idx) for r in bwt_records]}')
        print(f' * Last: {[r.last_ch + str(r.last_ch_idx) for r in bwt_records]}')
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
    seq_rotations = rotate_right(seq)
    seq_rotations_sorted = sorted(
        seq_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp_char_only(a[0], b[0], end_marker))
    )
    last_col_seq = ''.join(row[-1] for row in seq_rotations_sorted)
    return to_bwt_from_last_sequence(last_col_seq, end_marker)
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
        print(f' * First: {[r.first_ch + str(r.first_ch_idx) for r in bwt_records]}')
        print(f' * Last: {[r.last_ch + str(r.last_ch_idx) for r in bwt_records]}')
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
    seq_rotations = rotate_right(seq)
    seq_rotations_sorted = sorted(
        seq_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp_char_only(a, b, end_marker))
    )
    first_ch_counter = Counter()
    last_ch_counter = Counter()
    ret = []
    for i, s in enumerate(seq_rotations_sorted):
        first_ch = s[0]
        first_ch_counter[first_ch] += 1
        first_ch_idx = first_ch_counter[first_ch]
        last_ch = s[-1]
        last_ch_counter[last_ch] += 1
        last_ch_idx = last_ch_counter[last_ch]
        record = BWTRecord(first_ch, first_ch_idx, last_ch, last_ch_idx)
        ret.append(record)
    # Populate record last-to-first pointers
    for i, record_a in enumerate(ret):
        last = record_a.last_ch, record_a.last_ch_idx
        for j, record_b in enumerate(ret):
            first = record_b.first_ch, record_b.first_ch_idx
            if last == first:
                record_a.last_to_first_idx = j
                break
    return ret
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
        print(f' * First: {[r.first_ch + str(r.first_ch_idx) for r in bwt_records]}')
        print(f' * Last: {[r.last_ch + str(r.last_ch_idx) for r in bwt_records]}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")









if __name__ == '__main__':
    main_optimized2_build()
