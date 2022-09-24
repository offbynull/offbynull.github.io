from __future__ import annotations

from sys import stdin

import yaml

from sequence_search import BurrowsWheelerTransform_Basic


# MARKDOWN_BUILD
class BWTRecord:
    __slots__ = ['first_ch', 'first_ch_cnt', 'last_ch', 'last_ch_cnt', 'last_to_first_idx']

    def __init__(self, first_ch: str, first_ch_cnt: int, last_ch: str, last_ch_cnt: int, last_to_first_idx: int):
        self.first_ch = first_ch
        self.first_ch_cnt = first_ch_cnt
        self.last_ch = last_ch
        self.last_ch_cnt = last_ch_cnt
        self.last_to_first_idx = last_to_first_idx


def to_bwt_records(
        seq: str,
        end_marker: str
) -> list[BWTRecord]:
    first, last = BurrowsWheelerTransform_Basic.get_bwt_first_and_last_columns(seq, end_marker)
    # Create cache of last-to-first pointers
    last_to_first = []
    for last_val in last:
        idx = next(i for i, first_val in enumerate(first) if last_val == first_val)
        last_to_first.append(idx)
    # Create records
    bwt_records = []
    for (first_ch, first_ch_cnt), (last_ch, last_ch_cnt), last_to_first_idx in zip(first, last, last_to_first):
        bwt_records.append(BWTRecord(first_ch, first_ch_cnt, last_ch, last_ch_cnt, last_to_first_idx))
    # Return
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
        bwt_records = to_bwt_records(seq, end_marker)
        print()
        print(f'The following first and last columns were produced ...')
        print()
        print(f' * First: {[(r.first_ch, r.first_ch_cnt) for r in bwt_records]}')
        print(f' * Last: {[(r.last_ch, r.last_ch_cnt) for r in bwt_records]}')
        print(f' * Last-to-First: {[r.last_to_first_idx for r in bwt_records]}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")














# MARKDOWN_WALK_AND_TEST
def walk(bwt_records: list[BWTRecord]) -> str:
    ret = ''
    row = 0  # first idx always has first_ch == end_marker because of the lexicographical sorting
    while True:
        ret += bwt_records[row].last_ch
        row = bwt_records[row].last_to_first_idx
        if row == 0:
            break
    ret = ret[::-1]  # reverse ret
    ret = ret[1:] + ret[0]  # ret has end_marker at beginning, rotate it to end
    return ret


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
# MARKDOWN_WALK_AND_TEST


def main_test():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        test = data['test']
        first = data['first']
        last = data['last']
        last_to_first = data['last_to_first']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records = []
        for (first_ch, first_ch_cnt), (last_ch, last_ch_cnt), last_to_first_idx in zip(first, last, last_to_first):
            bwt_records.append(BWTRecord(first_ch, first_ch_cnt, last_ch, last_ch_cnt, last_to_first_idx))
        print()
        found_cnt = find(bwt_records, test)
        print()
        print(f'*{test}* found {found_cnt} times.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")










if __name__ == '__main__':
    main_test()
