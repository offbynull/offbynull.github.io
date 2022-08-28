import functools
from bisect import bisect_left
from collections import Counter
from sys import stdin

import yaml

from helpers.Utils import rotate_right
from sequence_search.BurrowsWheelerTransform_Deserialization import cmp_char_only
from sequence_search.SearchUtils import StringView


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
    seq_rotations = rotate_right(seq)
    seq_rotations_sorted = sorted(
        seq_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp_char_only(a, b, end_marker))
    )
    prev_first_ch = None
    last_ch_counter = Counter()
    bwt_array = []
    bwt_first_occurrence_map = {}
    bwt_last_tallies_checkpoints = {}
    for i, s in enumerate(seq_rotations_sorted):
        first_ch = s[0]
        last_ch = s[-1]
        last_ch_counter[last_ch] += 1
        bwt_record = BWTRecord(last_ch)
        bwt_array.append(bwt_record)
        if i % last_tallies_checkpoint_n == 0:
            bwt_last_tallies_checkpoints[i] = last_ch_counter.copy()
        if first_ch != prev_first_ch:
            bwt_first_occurrence_map[first_ch] = i
            prev_first_ch = first_ch
    return bwt_array, bwt_first_occurrence_map, bwt_last_tallies_checkpoints
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
        r_strs = []
        for idx, last_tallies in bwt_last_tallies_checkpoints.items():
            tallies_str = ','.join(f"{k}={v}" for k, v in last_tallies.items())
            r_str = f'{idx}: {{{tallies_str}}}'
            r_strs.append(r_str)
        print(f' * Last tallies checkpoints: {{{", ".join(r_strs)}}}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")










# MARKDOWN_WALK_TALLIES_TO_CHECKPOINT
def walk_tallies_to_checkpoint(
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        idx: int
) -> Counter[str]:
    partial_tallies = Counter()
    while idx not in bwt_last_tallies_checkpoints:
        ch = bwt_records[idx].last_ch
        partial_tallies[ch] += 1
        idx -= 1
    return partial_tallies + bwt_last_tallies_checkpoints[idx]
# MARKDOWN_WALK_TALLIES_TO_CHECKPOINT


def main_walk_tallies_to_checkpoint():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        seq = data['sequence']
        end_marker = data['end_marker']
        last_tallies_checkpoint_n = data['last_tallies_checkpoint_n']
        index = data['index']
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
        r_strs = []
        for idx, tallies in bwt_last_tallies_checkpoints.items():
            tallies_str = ','.join(f"{k}={v}" for k, v in tallies.items())
            r_str = f'{idx}: {{{tallies_str}}}'
            r_strs.append(r_str)
        print(f' * Last tallies checkpoints: {{{", ".join(r_strs)}}}')
        print()
        tally = walk_tallies_to_checkpoint(bwt_records, bwt_last_tallies_checkpoints, index)
        print(f'The tally at index {index} is calculated as {{{",".join(f"{k}={v}" for k, v in tally.items())}}}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")










# MARKDOWN_SINGLE_TALLY_TO_CHECKPOINT
def single_tally_to_checkpoint(
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        idx: int
) -> int:
    tally_ch = bwt_records[idx].last_ch
    partial_tally = 0
    while idx not in bwt_last_tallies_checkpoints:
        ch = bwt_records[idx].last_ch
        if ch == tally_ch:
            partial_tally += 1
        idx -= 1
    return partial_tally + bwt_last_tallies_checkpoints[idx][tally_ch]
# MARKDOWN_SINGLE_TALLY_TO_CHECKPOINT


def main_single_tally_to_checkpoint():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        seq = data['sequence']
        end_marker = data['end_marker']
        last_tallies_checkpoint_n = data['last_tallies_checkpoint_n']
        index = data['index']
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
        r_strs = []
        for idx, tallies in bwt_last_tallies_checkpoints.items():
            tallies_str = ','.join(f"{k}={v}" for k, v in tallies.items())
            r_str = f'{idx}: {{{tallies_str}}}'
            r_strs.append(r_str)
        print(f' * Last tallies checkpoints: {{{", ".join(r_strs)}}}')
        print()
        tally = single_tally_to_checkpoint(bwt_records, bwt_last_tallies_checkpoints, index)
        print(f'The tally for character {bwt_records[index].last_ch} at index {index} is calculated as {tally}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")











# MARKDOWN_TEST
def to_symbol_instance_count(
        bwt_records: list[BWTRecord],
        bwt_last_tallies: dict[int, Counter[str]],
        idx: int
) -> int:
    return single_tally_to_checkpoint(bwt_records, bwt_last_tallies, idx)


def to_first_index(
        bwt_first_occurrence_map: dict[str, int],
        symbol_instance: tuple[str, int]
) -> int:
    symbol, symbol_count = symbol_instance
    return bwt_first_occurrence_map[symbol] + symbol_count - 1


def find(
        bwt_records: list[BWTRecord],
        bwt_first_occurrence_map: dict[str, int],
        bwt_last_tallies: dict[int, Counter[str]],
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
                last_ch_idx = to_symbol_instance_count(bwt_records, bwt_last_tallies, i)
                last_to_first_idx = to_first_index(
                    bwt_first_occurrence_map,
                    (record.last_ch, last_ch_idx)
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
        last_tallies_checkpoint_n = data['last_tallies_checkpoint_n']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records, bwt_first_occurrence_map, bwt_last_tallies_checkpoints = to_bwt_ranked_checkpointed(seq, end_marker, last_tallies_checkpoint_n)
        print()
        print(f'The following first and last columns were produced ...')
        print()
        print(f' * First (squashed): {bwt_first_occurrence_map}')
        print(f' * Last: {[r.last_ch for r in bwt_records]}')
        r_strs = []
        for idx, tallies in bwt_last_tallies_checkpoints.items():
            tallies_str = ','.join(f"{k}={v}" for k, v in tallies.items())
            r_str = f'{idx}: {{{tallies_str}}}'
            r_strs.append(r_str)
        print(f' * Last tallies checkpoints: {{{", ".join(r_strs)}}}')
        print()
        found_cnt = find(bwt_records, bwt_first_occurrence_map, bwt_last_tallies_checkpoints, test)
        print()
        print(f'*{test}* found in *{seq}* {found_cnt} times.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")








if __name__ == '__main__':
    main_test()