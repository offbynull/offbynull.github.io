import functools
from collections import Counter
from sys import stdin
from typing import Iterator

import yaml

from sequence_search.BurrowsWheelerTransform_Deserialization import cmp_symbol
from sequence_search.SearchUtils import RotatedStringView, to_seeds, hamming_distance


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
        key=functools.cmp_to_key(lambda a, b: cmp_symbol(a[1], b[1], end_marker))
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
        # index = bwt_records[index].last_to_first_ptr
        # walk_cnt += 1
        #
        # UPDATED CODE
        # ------------
        # The updated version's "last_to_first_ptr" is computed dynamically using the pieces
        # from the ranked checkpoint algorithm. First it derives the symbol instance count
        # for bwt_record[index] using ranked checkpoints, then it converts that to the
        # "last_to_first_ptr" value via to_first_index().
        last_ch = bwt_records[index].last_ch
        last_ch_cnt = to_last_symbol_instance_count(bwt_records, bwt_last_tallies_checkpoints, index)
        index = to_first_row(bwt_first_occurrence_map, (last_ch, last_ch_cnt))
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


def to_last_symbol_instance_count(
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        idx: int
) -> int:
    return single_tally_to_checkpoint(bwt_records, bwt_last_tallies_checkpoints, idx, bwt_records[idx].last_ch)


def to_first_row(
        bwt_first_occurrence_map: dict[str, int],
        symbol_instance: tuple[str, int]
) -> int:
    symbol, symbol_count = symbol_instance
    return bwt_first_occurrence_map[symbol] + symbol_count - 1


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
        bwt_first_indexes_checkpoints: dict[int, int],
        bwt_first_occurrence_map: dict[str, int],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        test: str
) -> list[int]:
    top = 0
    bottom = len(bwt_records) - 1
    for i, ch in reversed(list(enumerate(test))):
        first_row_for_ch = bwt_first_occurrence_map.get(ch, None)
        if first_row_for_ch is None:  # ch must be in first occurrence map, otherwise it's not in the original seq
            return []
        top = first_row_for_ch + last_tally_before_row(ch, top, bwt_records, bwt_last_tallies_checkpoints)
        bottom = first_row_for_ch + last_tally_at_row(ch, bottom, bwt_records, bwt_last_tallies_checkpoints) - 1
        if top > bottom:  # top>bottom once the scan reaches a point in the test sequence where it's not in original seq
            return []
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











# MARKDOWN_MISMATCH
# This function has two ways of extracting out the segment of the original sequence to use for a mismatch test:
#
#  1. pull it out from the original sequence directly (a copy of it is in this func)
#  2. pull it out by walking the BWT matrix last-to-first (as is done in walk_back_until_first_index_checkpoint)
#
# This function uses #2 (#1 is still here but commented out). The reason is that, for the challenge problem, we're not
# supposed to have the original sequence at all. The challenge problem gives an already constructed copy of bwt_records
# and bwt_first_indexes_checkpoints, meaning that it wants us to use #2. I reconstructed the original sequence from that
# already provided bwt_records via ...
#
#     bwt_records = BurrowsWheelerTransform_Deserialization.to_bwt_from_last_sequence(last_seq, '$')
#     test_seq = BurrowsWheelerTransform_Basic.walk(bwt_records)
#
# It was reconstructed because it makes the code for the challenge problem cleaner (it just calls into this function,
# which does all the BWT setup from the original sequence and follows through with finding matches). However, that
# cleaner code is technically wasting a bunch of memory because the challenge problem already gave bwt_records and
# bwt_first_indexes_checkpoints.
def mismatch_search(
        test_seq: str,
        search_seqs: set[str] | list[str] | Iterator[str],
        max_mismatch: int,
        end_marker: str,
        pad_marker: str,
        last_tallies_checkpoint_n: int = 50,
        first_idxes_checkpoint_n: int = 50,
) -> set[tuple[int, str, str, int]]:
    # Add end marker and padding to test sequence
    assert end_marker not in test_seq, f'{test_seq} should not contain end marker'
    assert pad_marker not in test_seq, f'{test_seq} should not contain pad marker'
    padding = pad_marker * max_mismatch
    test_seq = padding + test_seq + padding + end_marker
    # Construct BWT data structure from original sequence
    checkpointed_bwt = to_bwt_checkpointed(
        test_seq,
        end_marker,
        last_tallies_checkpoint_n,
        first_idxes_checkpoint_n
    )
    bwt_records, bwt_first_occurrence_map, bwt_last_tallies_checkpoints, bwt_first_indexes_checkpoints = checkpointed_bwt
    # Flip around bwt_first_indexes_checkpoints so that instead of being bwt_row -> first_idx, it becomes
    # first_idx -> bwt_row. This is required for the last-to-first extraction process (option #2) because, when you get
    # an index within the original sequence, you can quickly map it to its corresponding bwt_records index.
    first_index_to_bwt_row = {}
    for bwt_row, first_idx in bwt_first_indexes_checkpoints.items():
        first_index_to_bwt_row[first_idx] = bwt_row
    # For each search_seq, break it up into seeds and find the indexes within test_seq based on that seed
    found_set = set()
    for i, search_seq in enumerate(search_seqs):
        seeds = to_seeds(search_seq, max_mismatch)
        seed_offset = 0
        for seed in seeds:
            # Pull out indexes in the original sequence where seed is
            test_seq_idxes = find(
                bwt_records,
                bwt_first_indexes_checkpoints,
                bwt_first_occurrence_map,
                bwt_last_tallies_checkpoints,
                seed
            )
            # Pull out relevant parts of the original sequence and test for mismatches
            for test_seq_start_idx in test_seq_idxes:
                # Extract segment original sequence
                test_seq_end_idx = test_seq_start_idx + len(search_seq)
                # OPTION #1: Extract from test_seq directly
                # -----------------------------------------
                # extracted_test_seq_segment = test_seq[test_seq_start_idx:test_seq_end_idx]
                #
                # OPTION #@: Extract by walking last-to-first
                # -------------------------------------------
                _, test_seq_end_idx_moved_up_to_first_idxes_checkpoint = closest_multiples(
                    test_seq_end_idx,
                    first_idxes_checkpoint_n
                )
                if test_seq_end_idx_moved_up_to_first_idxes_checkpoint >= len(bwt_records):
                    extraction_bwt_row = len(bwt_records) - 1
                else:
                    extraction_bwt_row = first_index_to_bwt_row[test_seq_end_idx_moved_up_to_first_idxes_checkpoint]
                extraction_len = test_seq_end_idx_moved_up_to_first_idxes_checkpoint - test_seq_start_idx
                extracted_test_seq_segment = walk_back_and_extract(
                    bwt_records,
                    bwt_first_occurrence_map,
                    bwt_last_tallies_checkpoints,
                    extraction_bwt_row,
                    extraction_len
                )
                extracted_test_seq_segment = extracted_test_seq_segment[:len(search_seq)]  # trim off to only part we're interestd in
                # Get mismatches between extracted segment of original sequence and search_seq, add if <= max_mismatches
                dist = hamming_distance(search_seq, extracted_test_seq_segment)
                if dist <= max_mismatch:
                    test_seq_segment = extracted_test_seq_segment
                    test_seq_idx_unpadded = test_seq_start_idx - len(padding)
                    found = test_seq_idx_unpadded, search_seq, test_seq_segment, dist
                    found_set.add(found)
            # Move up seed offset
            seed_offset += len(seed)
    # Return found items
    return found_set


# This function uses last-to-first walking to extract a portion of the original sequence used to create the BWT matrix,
# similar to the last-to-first walking done to find first index: walk_back_until_first_index_checkpoint().
def walk_back_and_extract(
        bwt_records: list[BWTRecord],
        bwt_first_occurrence_map: dict[str, int],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        row: int,
        count: int
) -> str:
    ret = ''
    while count > 0:
        # PREVIOUS CODE
        # -------------
        # ret += bwt_records[index].last_ch
        # index = bwt_records[index].last_to_first_idx
        # count -= 1
        #
        # UPDATED CODE
        # ------------
        ret += bwt_records[row].last_ch
        last_ch = bwt_records[row].last_ch
        last_ch_cnt = to_last_symbol_instance_count(bwt_records, bwt_last_tallies_checkpoints, row)
        row = to_first_row(bwt_first_occurrence_map, (last_ch, last_ch_cnt))
        count -= 1
    ret = ret[::-1]  # reverse ret
    return ret


# This function finds the closest multiple of n that's <= idx and closest multiple of n that's >= idx
def closest_multiples(idx: int, multiple: int) -> tuple[int, int]:
    if idx % multiple == 0:
        start_idx_at_multiple = (idx // multiple * multiple)
        stop_idx_at_multiple = start_idx_at_multiple
    else:
        start_idx_at_multiple = (idx // multiple * multiple)
        stop_idx_at_multiple = (idx // multiple * multiple) + multiple
    return start_idx_at_multiple, stop_idx_at_multiple
# MARKDOWN_MISMATCH


def main_mismatch():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        test_seq = data['sequence']
        search_seqs = set(s for s in data['search_sequences'])
        end_marker = data['end_marker']
        pad_marker = data['pad_marker']
        max_mismatch = data['max_mismatch']
        first_indexes_checkpoint_n = data['first_indexes_checkpoint_n']
        last_tallies_checkpoint_n = data['last_tallies_checkpoint_n']
        print(f'Building and searching trie using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        found_set = mismatch_search(test_seq, search_seqs, max_mismatch, end_marker, pad_marker, last_tallies_checkpoint_n, first_indexes_checkpoint_n)
        print()
        print(f'Searching `{search_seqs}` revealed the following was found:')
        print()
        for found_idx, actual, found, dist in sorted(found_set):
            print(f' * Matched `{found}` against `{actual}` with distance of {dist} at index {found_idx}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")




if __name__ == '__main__':
    main_mismatch()
