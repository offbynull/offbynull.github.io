import functools
from collections import Counter
from sys import stdin

import yaml

from sequence_search.BurrowsWheelerTransform_Deserialization import cmp_symbol
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
        key=functools.cmp_to_key(lambda a, b: cmp_symbol(a, b, end_marker))
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
        print(f' * Last: {[(r.last_ch, r.last_ch_cnt) for r in bwt_records]}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")











# MARKDOWN_FIRST_INDEX
def to_first_row(
        bwt_first_occurrence_map: dict[str, int],
        symbol_instance: tuple[str, int]
) -> int:
    symbol, symbol_count = symbol_instance
    return bwt_first_occurrence_map[symbol] + symbol_count - 1
# MARKDOWN_FIRST_INDEX


# MARKDOWN_LAST_TO_FIRST
# This is just a wrapper for to_first_row(). It's here for clarity.
def last_to_first(
        bwt_first_occurrence_map: dict[str, int],
        symbol_instance: tuple[str, int]
) -> int:
    return to_first_row(bwt_first_occurrence_map, symbol_instance)
# MARKDOWN_LAST_TO_FIRST


def main_first_index():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        first_occurrence_map = data['first_occurrence_map']
        last = data['last']
        last_to_first = data['last_to_first']
        symbol = data['symbol']
        symbol_count = data['symbol_count']
        print(print(f'Finding the first column index using the following settings...'))
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records = []
        for last_ch, last_ch_cnt in last:
            bwt_records.append(BWTRecord(last_ch, last_ch_cnt))
        first_row = to_first_row(first_occurrence_map, (symbol, symbol_count))
        print()
        print(f'The index of {symbol}{symbol_count} in the first column is: {first_row}')
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
                # last_to_first is now calculated on-the-fly
                last_to_first_ptr = last_to_first(
                    bwt_first_occurrence_map,
                    (record.last_ch, record.last_ch_cnt)
                )
                new_top = min(new_top, last_to_first_ptr)
                new_bottom = max(new_bottom, last_to_first_ptr)
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
        first_occurrence_map = data['first_occurrence_map']
        last = data['last']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records = []
        for last_ch, last_ch_cnt in last:
            bwt_records.append(BWTRecord(last_ch, last_ch_cnt))
        found_cnt = find(bwt_records, first_occurrence_map, test)
        print()
        print(f'*{test}* found {found_cnt} times.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")









# MARKDOWN_TEST_INITIAL_PASS_OPTIMIZED
def get_top_bottom_range_for_first(
        bwt_records: list[BWTRecord],
        bwt_first_occurrence_map: dict[str, int],
        ch: str
):
    # End marker will always have been in idx 0 of first
    end_marker = next(first_ch for first_ch, row in bwt_first_occurrence_map.items() if row == 0)
    sorted_keys = sorted(
        bwt_first_occurrence_map.keys(),
        key=functools.cmp_to_key(lambda a, b: cmp_symbol(a, b, end_marker))
    )
    sorted_keys_idx = sorted_keys.index(ch)  # It's possible to replace this with binary search, because keys are sorted
    sorted_keys_next_idx = sorted_keys_idx + 1
    if sorted_keys_next_idx >= len(sorted_keys):
        top = bwt_first_occurrence_map[ch]
        bottom = len(bwt_records) - 1
    else:
        ch_next = sorted_keys[sorted_keys_next_idx]
        top = bwt_first_occurrence_map[ch]
        bottom = bwt_first_occurrence_map[ch_next] - 2
    return top, bottom


def find_optimized(
        bwt_records: list[BWTRecord],
        bwt_first_occurrence_map: dict[str, int],
        test: str
) -> int:
    # Use bwt_first_occurrence_map to determine top&bottom for last char rather than starting off with  a full scan
    top, bottom = get_top_bottom_range_for_first(
        bwt_records,
        bwt_first_occurrence_map,
        test[-1]
    )
    # Since the code above already calculated top&bottom for last char, trim it off before going into the isolation loop
    test = test[:-1]
    for ch in reversed(test):
        new_top = len(bwt_records)
        new_bottom = -1
        for i in range(top, bottom + 1):
            record = bwt_records[i]
            if ch == record.last_ch:
                # last_to_first is now calculated on-the-fly
                last_to_first_idx = last_to_first(
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
# MARKDOWN_TEST_INITIAL_PASS_OPTIMIZED


def main_test_optimized():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        test = data['test']
        first_occurrence_map = data['first_occurrence_map']
        last = data['last']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records = []
        for last_ch, last_ch_cnt in last:
            bwt_records.append(BWTRecord(last_ch, last_ch_cnt))
        found_cnt = find(bwt_records, first_occurrence_map, test)
        print()
        print(f'*{test}* found {found_cnt} times.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")







if __name__ == '__main__':
    # main_table_and_collapsed_first()
    main_first_index()
    # main_test()
