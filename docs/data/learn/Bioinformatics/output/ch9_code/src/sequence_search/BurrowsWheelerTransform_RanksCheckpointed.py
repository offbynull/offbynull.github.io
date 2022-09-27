import functools
from collections import Counter
from sys import stdin

import yaml

from sequence_search.BurrowsWheelerTransform_Deserialization import cmp_symbol
from sequence_search.SearchUtils import RotatedStringView


# MARKDOWN_BUILD_RANKED_CHECKPOINTED
class BWTRecord:
    __slots__ = ['last_ch']

    def __init__(self, last_ch: str):
        self.last_ch = last_ch


def to_bwt_ranked_checkpointed(
        seq: str,
        end_marker: str,
        last_tallies_checkpoint_n: int
) -> tuple[list[BWTRecord], dict[str, int], dict[int, Counter[str]]]:
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
    bwt_last_tallies_checkpoints = {}
    for i, s in enumerate(seq_rotations_sorted):
        first_ch = s[0]
        last_ch = s[-1]
        last_ch_counter[last_ch] += 1
        bwt_record = BWTRecord(last_ch)
        bwt_records.append(bwt_record)
        if i % last_tallies_checkpoint_n == 0:
            bwt_last_tallies_checkpoints[i] = last_ch_counter.copy()
        if first_ch != prev_first_ch:
            bwt_first_occurrence_map[first_ch] = i
            prev_first_ch = first_ch
    return bwt_records, bwt_first_occurrence_map, bwt_last_tallies_checkpoints
# MARKDOWN_BUILD_RANKED_CHECKPOINTED


def main_build():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        seq = data['sequence']
        end_marker = data['end_marker']
        last_tallies_checkpoint_n = data['last_tallies_checkpoint_n']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records, bwt_first_occurrence_map, bwt_last_tallies_checkpoints = to_bwt_ranked_checkpointed(seq, end_marker, last_tallies_checkpoint_n)
        print()
        print(f'The following last column and squashed first mapping were produced ...')
        print()
        print(f' * First (squashed): {bwt_first_occurrence_map}')
        print(f' * Last: {[r.last_ch for r in bwt_records]}')
        bwt_last_tallies_checkpoints = {k: dict(v) for k, v in bwt_last_tallies_checkpoints.items()}
        print(f' * Last Tallies Checkpoints: {bwt_last_tallies_checkpoints}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")










# MARKDOWN_WALK_TALLIES_TO_CHECKPOINT
def walk_tallies_to_checkpoint(
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        row: int
) -> Counter[str]:
    partial_tallies = Counter()
    while row not in bwt_last_tallies_checkpoints:
        ch = bwt_records[row].last_ch
        partial_tallies[ch] += 1
        row -= 1
    return partial_tallies + bwt_last_tallies_checkpoints[row]
# MARKDOWN_WALK_TALLIES_TO_CHECKPOINT


def main_walk_tallies_to_checkpoint():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        last = data['last']
        last_tallies_checkpoints = data['last_tallies_checkpoints']
        index = data['index']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        last_tallies_checkpoints = {k: Counter(v) for k, v in last_tallies_checkpoints.items()}
        bwt_records = []
        for last_ch in last:
            bwt_records.append(BWTRecord(last_ch))
        tally = walk_tallies_to_checkpoint(bwt_records, last_tallies_checkpoints, index)
        print(f'The tally at index {index} is calculated as {tally.items}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")










# MARKDOWN_SINGLE_TALLY_TO_CHECKPOINT
def single_tally_to_checkpoint(
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        row: int,
        tally_ch: str
) -> int:
    partial_tally = 0
    while row not in bwt_last_tallies_checkpoints:
        ch = bwt_records[row].last_ch
        if ch == tally_ch:
            partial_tally += 1
        row -= 1
    return partial_tally + bwt_last_tallies_checkpoints[row][tally_ch]
# MARKDOWN_SINGLE_TALLY_TO_CHECKPOINT


def main_single_tally_to_checkpoint():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        last = data['last']
        last_tallies_checkpoints = data['last_tallies_checkpoints']
        index = data['index']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        last_tallies_checkpoints = {k: Counter(v) for k, v in last_tallies_checkpoints.items()}
        bwt_records = []
        for last_ch in last:
            bwt_records.append(BWTRecord(last_ch))
        tally = single_tally_to_checkpoint(bwt_records, last_tallies_checkpoints, index, bwt_records[index].last_ch)
        print(f'The tally for character {bwt_records[index].last_ch} at index {index} is calculated as {tally}')
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


def to_last_symbol_instance_count(
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        row: int
) -> int:
    return single_tally_to_checkpoint(bwt_records, bwt_last_tallies_checkpoints, row, bwt_records[row].last_ch)

# MARKDOWN_TEST
def last_tally_before_row(
        symbol: str,
        row: int,
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]]
):
    ch_incremented_at_row = bwt_records[row].last_ch == symbol
    ch_tally = single_tally_to_checkpoint(bwt_records, bwt_last_tallies_checkpoints, row, symbol)
    if ch_incremented_at_row:
        ch_tally -= 1
    return ch_tally


def last_tally_at_row(
        symbol: str,
        row: int,
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]]
):
    ch_tally = single_tally_to_checkpoint(bwt_records, bwt_last_tallies_checkpoints, row, symbol)
    return ch_tally


def find(
        bwt_records: list[BWTRecord],
        bwt_first_occurrence_map: dict[str, int],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        test: str
) -> int:
    top_row = 0
    bottom_row = len(bwt_records) - 1
    for i, ch in reversed(list(enumerate(test))):
        first_row_for_ch = bwt_first_occurrence_map.get(ch, None)
        if first_row_for_ch is None:  # ch must be in first occurrence map, otherwise it's not in the original seq
            return 0
        top_symbol_instance = ch, last_tally_before_row(ch, top_row, bwt_records, bwt_last_tallies_checkpoints) + 1
        top_row = last_to_first(bwt_first_occurrence_map, top_symbol_instance)
        bottom_symbol_instance = ch, last_tally_at_row(ch, bottom_row, bwt_records, bwt_last_tallies_checkpoints)
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
        last_tallies_checkpoints = data['last_tallies_checkpoints']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        last_tallies_checkpoints = {k: Counter(v) for k, v in last_tallies_checkpoints.items()}
        bwt_records = []
        for last_ch in last:
            bwt_records.append(BWTRecord(last_ch))
        found_cnt = find(bwt_records, first_occurrence_map, last_tallies_checkpoints, test)
        print()
        print(f'*{test}* found {found_cnt} times.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")








if __name__ == '__main__':
    main_walk_tallies_to_checkpoint()
