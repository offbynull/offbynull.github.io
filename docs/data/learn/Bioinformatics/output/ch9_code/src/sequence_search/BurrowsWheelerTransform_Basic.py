import functools
from collections import Counter
from sys import stdin

import yaml

from helpers.Utils import rotate_right


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
    __slots__ = ['first_ch', 'first_ch_idx', 'last_ch', 'last_ch_idx', 'last_to_first_idx']

    def __init__(self, first_ch: str, first_ch_idx: int, last_ch: str, last_ch_idx: int):
        self.first_ch = first_ch
        self.first_ch_idx = first_ch_idx
        self.last_ch = last_ch
        self.last_ch_idx = last_ch_idx
        self.last_to_first_idx = -1

    def __str__(self):
        return str((self.first_ch + str(self.first_ch_idx), self.last_ch + str(self.last_ch_idx), self.last_to_first_idx))

    def __repr__(self):
        return str(self)


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
        print(f' * First: {[r.first_ch + str(r.first_ch_idx) for r in bwt_records]}')
        print(f' * Last: {[r.last_ch + str(r.last_ch_idx) for r in bwt_records]}')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")









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
        print(f' * First: {[r.first_ch + str(r.first_ch_idx) for r in bwt_records]}')
        print(f' * Last: {[r.last_ch + str(r.last_ch_idx) for r in bwt_records]}')
        print()
        found_cnt = find(bwt_records, test)
        print()
        print(f'*{test}* found in *{seq}* at {found_cnt} times.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")











if __name__ == '__main__':
    main_build()