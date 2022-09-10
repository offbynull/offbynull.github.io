import functools
from collections import Counter
from sys import stdin

import yaml

from sequence_search.BurrowsWheelerTransform_Deserialization import cmp_char_only
from sequence_search.SearchUtils import RotatedStringView


# MARKDOWN_BUILD
class BWTRecord:
    __slots__ = ['last_ch']

    def __init__(self, last_ch: str):
        self.last_ch = last_ch


def to_bwt_checkpointed(
        seq: str,
        end_marker: str,
        last_tallies_checkpoint_n: int,
        first_indexes_checkpoint_n: int
) -> tuple[list[BWTRecord], dict[str, int], dict[int, Counter[str]], dict[int, int]]:
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    seq_with_counts_rotations = [(i, RotatedStringView(i, seq)) for i in range(len(seq))]  # rotations + new first_idx for each rotation
    seq_with_counts_rotations_sorted = sorted(
        seq_with_counts_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp_char_only(a[1], b[1], end_marker))
    )
    prev_first_ch = None
    last_ch_counter = Counter()
    bwt_records = []
    bwt_first_occurrence_map = {}
    bwt_last_tallies_checkpoints = {}
    bwt_first_indexes_checkpoints = {}
    for i, (first_idx, s) in enumerate(seq_with_counts_rotations_sorted):
        first_ch = s[0]
        last_ch = s[-1]
        last_ch_counter[last_ch] += 1
        bwt_record = BWTRecord(last_ch)
        bwt_records.append(bwt_record)
        if i % last_tallies_checkpoint_n == 0:
            bwt_last_tallies_checkpoints[i] = last_ch_counter.copy()
        if first_idx % first_indexes_checkpoint_n == 0:
            bwt_first_indexes_checkpoints[i] = first_idx
        if first_ch != prev_first_ch:
            bwt_first_occurrence_map[first_ch] = i
            prev_first_ch = first_ch
    return bwt_records, bwt_first_occurrence_map, bwt_last_tallies_checkpoints, bwt_first_indexes_checkpoints
# MARKDOWN_BUILD


def main_build():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        seq = data['sequence']
        end_marker = data['end_marker']
        last_tallies_checkpoint_n = data['last_tallies_checkpoint_n']
        first_indexes_checkpoint_n = data['first_indexes_checkpoint_n']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        ret = to_bwt_checkpointed(seq, end_marker, last_tallies_checkpoint_n, first_indexes_checkpoint_n)
        bwt_records, bwt_first_occurrence_map, bwt_last_tallies_checkpoints, bwt_first_indexes_checkpoints = ret
        print()
        print(f'The following last column and squashed first mapping were produced ...')
        print()
        print(f' * First (squashed): {bwt_first_occurrence_map}')
        print(f' * First Index Checkpoints: {bwt_first_indexes_checkpoints}')
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












































# MARKDOWN_WALK_BACK_TO_FIRST_IDX
def walk_back_until_first_index_checkpoint(
        bwt_records: list[BWTRecord],
        bwt_first_indexes_checkpoints: dict[int, int],
        bwt_first_occurrence_map: dict[str, int],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        index: int
) -> int:
    walk_cnt = 0
    while index not in bwt_first_indexes_checkpoints:
        # ORIGINAL CODE
        # -------------
        # index = bwt_records[index].last_to_first_idx
        # walk_cnt += 1
        #
        # UPDATED CODE
        # ------------
        # The updated version's "last_to_first_idx" is computed dynamically using the pieces
        # from the ranked checkpoint algorithm. First it derives the symbol instance count
        # for bwt_record[index] using ranked checkpoints, then it converts that to the
        # "last_to_first_idx" value via to_first_index().
        last_ch = bwt_records[index].last_ch
        last_ch_cnt = to_symbol_instance_count(bwt_records, bwt_last_tallies_checkpoints, index)
        index = to_first_index(bwt_first_occurrence_map, (last_ch, last_ch_cnt))
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
        last_tallies_checkpoint_n = data['last_tallies_checkpoint_n']
        first_indexes_checkpoint_n = data['first_indexes_checkpoint_n']
        from_index = data['from_index']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        ret = to_bwt_checkpointed(seq, end_marker, last_tallies_checkpoint_n, first_indexes_checkpoint_n)
        bwt_records, bwt_first_occurrence_map, bwt_last_tallies_checkpoints, bwt_first_indexes_checkpoints = ret
        print()
        print(f'The following last column and squashed first mapping were produced ...')
        print()
        print(f' * First (squashed): {bwt_first_occurrence_map}')
        print(f' * First Index Checkpoints: {bwt_first_indexes_checkpoints}')
        print(f' * Last: {[r.last_ch for r in bwt_records]}')
        r_strs = []
        for idx, last_tallies in bwt_last_tallies_checkpoints.items():
            tallies_str = ','.join(f"{k}={v}" for k, v in last_tallies.items())
            r_str = f'{idx}: {{{tallies_str}}}'
            r_strs.append(r_str)
        print(f' * Last tallies checkpoints: {{{", ".join(r_strs)}}}')
        print()
        first_idx = walk_back_until_first_index_checkpoint(bwt_records, bwt_first_indexes_checkpoints, bwt_first_occurrence_map, bwt_last_tallies_checkpoints, from_index)
        print(f'Walking back to a first index checkpoint resulted in a first index of {first_idx} ...')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")







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


def to_symbol_instance_count(
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        idx: int
) -> int:
    return single_tally_to_checkpoint(bwt_records, bwt_last_tallies_checkpoints, idx)


def to_first_index(
        bwt_first_occurrence_map: dict[str, int],
        symbol_instance: tuple[str, int]
) -> int:
    symbol, symbol_count = symbol_instance
    return bwt_first_occurrence_map[symbol] + symbol_count - 1


# MARKDOWN_TEST
def find(
        bwt_records: list[BWTRecord],
        bwt_first_indexes_checkpoints: dict[int, int],
        bwt_first_occurrence_map: dict[str, int],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        test: str
) -> list[int]:
    top = 0
    bottom = len(bwt_records) - 1
    for ch in reversed(test):
        new_top = len(bwt_records)
        new_bottom = -1
        for i in range(top, bottom + 1):
            record = bwt_records[i]
            if ch == record.last_ch:
                last_ch_cnt = to_symbol_instance_count(bwt_records, bwt_last_tallies_checkpoints, i)
                last_to_first_idx = to_first_index(
                    bwt_first_occurrence_map,
                    (record.last_ch, last_ch_cnt)
                )
                new_top = min(new_top, last_to_first_idx)
                new_bottom = max(new_bottom, last_to_first_idx)
        if new_bottom == -1 or new_top == len(bwt_records):  # technically only need to check one of these conditions
            return []
        top = new_top
        bottom = new_bottom
    # Find first_index for each entry in between top and bottom
    first_idxes = []
    for index in range(top, bottom + 1):
        first_idx = walk_back_until_first_index_checkpoint(
            bwt_records,
            bwt_first_indexes_checkpoints,
            bwt_first_occurrence_map,
            bwt_last_tallies_checkpoints,
            index
        )
        first_idxes.append(first_idx)
    return first_idxes
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
        first_indexes_checkpoint_n = data['first_indexes_checkpoint_n']
        last_tallies_checkpoint_n = data['last_tallies_checkpoint_n']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        ret = to_bwt_checkpointed(seq, end_marker, last_tallies_checkpoint_n, first_indexes_checkpoint_n)
        bwt_records, bwt_first_occurrence_map, bwt_last_tallies_checkpoints, bwt_first_indexes_checkpoints = ret
        print()
        print(f'The following last column and squashed first mapping were produced ...')
        print()
        print(f' * First (squashed): {bwt_first_occurrence_map}')
        print(f' * First Index Checkpoints: {bwt_first_indexes_checkpoints}')
        print(f' * Last: {[r.last_ch for r in bwt_records]}')
        r_strs = []
        for idx, last_tallies in bwt_last_tallies_checkpoints.items():
            tallies_str = ','.join(f"{k}={v}" for k, v in last_tallies.items())
            r_str = f'{idx}: {{{tallies_str}}}'
            r_strs.append(r_str)
        print(f' * Last tallies checkpoints: {{{", ".join(r_strs)}}}')
        print()
        found_cnt = find(bwt_records, bwt_first_indexes_checkpoints, bwt_first_occurrence_map, bwt_last_tallies_checkpoints, test)
        print()
        print(f'*{test}* found in *{seq}* at indices {found_cnt}.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")








if __name__ == '__main__':
    main_test()
