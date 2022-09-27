import functools
from collections import Counter
from sys import stdin

import yaml

from sequence_search.BurrowsWheelerTransform_Deserialization import cmp_symbol
from sequence_search.SearchUtils import RotatedStringView


# MARKDOWN_BUILD_RANKED
class BWTRecord:
    __slots__ = ['last_ch', 'last_tallies']

    def __init__(self, last_ch: str, last_tallies: Counter[str]):
        self.last_ch = last_ch
        self.last_tallies = last_tallies


def to_bwt_ranked(
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
        bwt_record = BWTRecord(last_ch, last_ch_counter.copy())
        bwt_records.append(bwt_record)
        if first_ch != prev_first_ch:
            bwt_first_occurrence_map[first_ch] = i
            prev_first_ch = first_ch
    return bwt_records, bwt_first_occurrence_map
# MARKDOWN_BUILD_RANKED


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
        bwt_records, bwt_first_occurrence_map = to_bwt_ranked(seq, end_marker)
        print()
        print(f'The following last column and squashed first mapping were produced ...')
        print()
        print(f' * First (collapsed): {bwt_first_occurrence_map}')
        print(f' * Last: {[r.last_ch for r in bwt_records]}')
        print(f' * Last Tallies: {[dict(r.last_tallies) for r in bwt_records]}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")









# MARKDOWN_TO_SYMBOL_INSTANCE_COUNT
def to_symbol_instance_count(rec: BWTRecord) -> int:
    ch = rec.last_ch
    return rec.last_tallies[ch]
# MARKDOWN_TO_SYMBOL_INSTANCE_COUNT


def main_to_symbol_instance_count():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        last_ch = data['last_ch']
        last_tallies = data['last_tallies']
        print(f'Extracting symbol instance count using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_record = BWTRecord(last_ch, last_tallies)
        print()
        print(f'The symbol instance count for this record is {to_symbol_instance_count(bwt_record)}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")







# MARKDOWN_TALLY_BEFORE
def last_tally_at_row(
        symbol: str,
        row: int,
        bwt_records: list[BWTRecord]
):
    ch_tally = bwt_records[row].last_tallies[symbol]
    return ch_tally


def last_tally_before_row(
        symbol: str,
        row: int,
        bwt_records: list[BWTRecord]
):
    ch_incremented_at_row = bwt_records[row].last_ch == symbol
    ch_tally = bwt_records[row].last_tallies[symbol]
    if ch_incremented_at_row:
        ch_tally -= 1
    return ch_tally
# MARKDOWN_TALLY_BEFORE


def main_tally_row():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        last = data['last']
        last_tallies = data['last_tallies']
        index = data['index']
        symbol = data['symbol']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records = []
        for last_ch, last_tallies_single in zip(last, last_tallies):
            bwt_records.append(BWTRecord(last_ch, last_tallies_single))
        found1 = last_tally_before_row(symbol, index, bwt_records)
        found2 = last_tally_at_row(symbol, index, bwt_records)
        print()
        print(f'There where {found1} instances of *{symbol}* just before reaching index *{index}* in last.')
        print()
        print(f'There where {found2} instances of *{symbol}* at index *{index}* in last.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")






def to_first_row(
        bwt_first_occurrence_map: dict[str, int],
        symbol_instance: tuple[str, int]
) -> int:
    symbol, symbol_count = symbol_instance
    return bwt_first_occurrence_map[symbol] + symbol_count - 1


def last_to_first(
        bwt_first_occurrence_map: dict[str, int],
        symbol_instance: tuple[str, int]
) -> int:
    return to_first_row(bwt_first_occurrence_map, symbol_instance)


# MARKDOWN_TEST
def find(
        bwt_records: list[BWTRecord],
        bwt_first_occurrence_map: dict[str, int],
        test: str
) -> int:
    top_row = 0
    bottom_row = len(bwt_records) - 1
    for i, ch in reversed(list(enumerate(test))):
        first_row_for_ch = bwt_first_occurrence_map.get(ch, None)
        if first_row_for_ch is None:  # ch must be in first occurrence map, otherwise it's not in the original seq
            return 0
        top_symbol_instance = ch, last_tally_before_row(ch, top_row, bwt_records) + 1
        top_row = last_to_first(bwt_first_occurrence_map, top_symbol_instance)
        bottom_symbol_instance = ch, last_tally_at_row(ch, bottom_row, bwt_records)
        bottom_row = last_to_first(bwt_first_occurrence_map, bottom_symbol_instance)
        if top_row > bottom_row:  # top>bottom once the scan reaches a point in the test sequence where it's not in original seq
            return 0
    return (bottom_row - top_row) + 1
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
        last_tallies = data['last_tallies']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records = []
        for last_ch, last_tallies_single in zip(last, last_tallies):
            bwt_records.append(BWTRecord(last_ch, last_tallies_single))
        found_cnt = find(bwt_records, first_occurrence_map, test)
        print()
        print(f'*{test}* found {found_cnt} times.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")








if __name__ == '__main__':
    main_test()
