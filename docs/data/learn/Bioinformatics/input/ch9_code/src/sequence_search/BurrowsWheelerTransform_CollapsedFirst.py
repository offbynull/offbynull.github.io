import functools
from collections import Counter
from sys import stdin

import yaml

from sequence_search.BurrowsWheelerTransform_Deserialization import cmp_char_only
from sequence_search.SearchUtils import RotatedStringView


# MARKDOWN_BUILD_TABLE_AND_COLLAPSED_FIRST
class BWTRecord:
    __slots__ = ['last_ch', 'last_ch_cnt']

    def __init__(self, last_ch: str, last_ch_cnt: int):
        self.last_ch = last_ch
        self.last_ch_cnt = last_ch_cnt


def to_bwt_and_first_occurrences(
        seq: str,
        end_marker: str
) -> tuple[list[BWTRecord], dict[str, int]]:
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    seq_rotations = [RotatedStringView(i, seq) for i in range(len(seq))]
    seq_rotations_sorted = sorted(
        seq_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp_char_only(a, b, end_marker))
    )
    prev_first_ch = None
    last_ch_counter = Counter()
    bwt_records = []
    bwt_first_occurrence_map = {}
    for i, s in enumerate(seq_rotations_sorted):
        first_ch = s[0]
        last_ch = s[-1]
        last_ch_counter[last_ch] += 1
        last_ch_cnt = last_ch_counter[last_ch]
        bwt_record = BWTRecord(last_ch, last_ch_cnt)
        bwt_records.append(bwt_record)
        if first_ch != prev_first_ch:
            bwt_first_occurrence_map[first_ch] = i
            prev_first_ch = first_ch
    return bwt_records, bwt_first_occurrence_map
# MARKDOWN_BUILD_TABLE_AND_COLLAPSED_FIRST


def main_table_and_collapsed_first():
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
        bwt_records, bwt_first_occurrence_map = to_bwt_and_first_occurrences(seq, end_marker)
        print()
        print(f'The following last column and collapsed first mapping were produced ...')
        print()
        print(f' * First (collapsed): {bwt_first_occurrence_map}')
        print(f' * Last: {[r.last_ch + str(r.last_ch_cnt) for r in bwt_records]}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")











# MARKDOWN_FIRST_INDEX
def to_first_index(
        bwt_first_occurrence_map: dict[str, int],
        symbol_instance: tuple[str, int]
) -> int:
    symbol, symbol_count = symbol_instance
    return bwt_first_occurrence_map[symbol] + symbol_count - 1
# MARKDOWN_FIRST_INDEX


def main_first_index():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        seq = data['sequence']
        end_marker = data['end_marker']
        symbol = data['symbol']
        symbol_count = data['symbol_count']
        print(print(f'Finding the first column index using the following settings...'))
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records, bwt_first_occurrence_map = to_bwt_and_first_occurrences(seq, end_marker)
        first_idx = to_first_index(bwt_first_occurrence_map, (symbol, symbol_count))
        print()
        print(f'The following last column and collapsed first mapping were produced ...')
        print()
        print(f' * First (collapsed): {bwt_first_occurrence_map}')
        print(f' * Last: {[r.last_ch + str(r.last_ch_cnt) for r in bwt_records]}')
        print()
        print(f'The index of {symbol}{symbol_count} in the first column is: {first_idx}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")










# MARKDOWN_TEST
def find(
        bwt_records: list[BWTRecord],
        bwt_first_occurrence_map: dict[str, int],
        test: str
) -> int:
    top = 0
    bottom = len(bwt_records) - 1
    for ch in reversed(test):
        new_top = len(bwt_records)
        new_bottom = -1
        for i in range(top, bottom + 1):
            record = bwt_records[i]
            if ch == record.last_ch:
                last_to_first_idx = to_first_index(
                    bwt_first_occurrence_map,
                    (record.last_ch, record.last_ch_cnt)
                )
                new_top = min(new_top, last_to_first_idx)
                new_bottom = max(new_bottom, last_to_first_idx)
        if new_bottom == -1 or new_top == len(bwt_records):  # technically only need to check one of these conditions
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
        bwt_records, bwt_first_occurrence_map = to_bwt_and_first_occurrences(seq, end_marker)
        print()
        print(f'The following first and last columns were produced ...')
        print()
        print(f' * First (collapsed): {bwt_first_occurrence_map}')
        print(f' * Last: {[r.last_ch + str(r.last_ch_cnt) for r in bwt_records]}')
        print()
        found_cnt = find(bwt_records, bwt_first_occurrence_map, test)
        print()
        print(f'*{test}* found in *{seq}* {found_cnt} times.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")








if __name__ == '__main__':
    # main_table_and_collapsed_first()
    # main_first_index()
    main_test()