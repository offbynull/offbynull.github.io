import tarfile
from collections import defaultdict
from typing import Counter

from sequence_search import BurrowsWheelerTransform_Deserialization, BurrowsWheelerTransform_Basic, \
    BurrowsWheelerTransform_Checkpointed
from sequence_search.SearchUtils import to_seeds, seed_extension


def mismatch_search(
        search_seq: str,
        bwt_records: list[BurrowsWheelerTransform_Checkpointed.BWTRecord],
        bwt_first_occurrence_map: dict[str, int],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        bwt_first_indexes_checkpoints: dict[int, int],
        max_mismatch: int,
        end_marker: str,
        pad_marker: str
):
    # Add padding to test sequence
    assert end_marker not in test_seq, f'{test_seq} should not contain end marker'
    assert pad_marker not in test_seq, f'{test_seq} should not contain pad marker'
    padding = pad_marker * max_mismatch
    test_seq = padding + test_seq + padding
    # Generate seeds from search_seqs
    seeds = to_seeds(test_seq, max_mismatch)
    # Scan for seeds
    found = {}
    found_seeds = set()
    for seed_idx, seed in enumerate(seeds):
        found_idxes = BurrowsWheelerTransform_Checkpointed.find(
            bwt_records,
            bwt_first_indexes_checkpoints,
            bwt_first_occurrence_map,
            bwt_last_tallies_checkpoints,
            test_seq)
        for found_idx in found_idxes:
            se_res = seed_extension(test_seq, found_idx, seed_idx, seeds)
            if se_res is None:
                continue
            test_seq_idx, dist = se_res
            if dist <= max_mismatch:
                found_value = test_seq[test_seq_idx:test_seq_idx + len(test_seq)]
                test_seq_idx_unpadded = test_seq_idx - len(padding)
                found = test_seq_idx_unpadded, search_seq, found_value, dist
                found.add(found)
                break


def main():
    # Extract original sequence from the problem's BWT last col.
    with tarfile.open('mycoplasma.tar.xz', 'r:xz') as t:
        with t.extractfile('mycoplasma/mycoplasma/myc_bwt.txt') as f:
            last_col = f.read().decode('utf-8').strip()
        bwt_records = BurrowsWheelerTransform_Deserialization.to_bwt_from_last_sequence(last_col, '$')
        orig_seq = BurrowsWheelerTransform_Basic.walk(bwt_records)
        bwt_records = None
        last_col = None

    max_mismatch = 1
    # Pad the sequence by the number of mismatches allowed (required for seed extension)
    padding = '_' * max_mismatch
    orig_seq = padding + orig_seq + padding
    # Push the sequence into the checkpointed BWT algorithm to create more optimized data structure
    print(f'out: {orig_seq[-1]}')
    checkpointed_bwt = BurrowsWheelerTransform_Checkpointed.to_bwt_checkpointed(orig_seq, '$', 1000, 1000)
    bwt_records, bwt_first_occurrence_map, bwt_last_tallies_checkpoints, bwt_first_indexes_checkpoints = checkpointed_bwt

    # Test against reads
    with tarfile.open('mycoplasma.tar.xz', 'r:xz') as t:
        with t.extractfile('mycoplasma/mycoplasma/myc_reads.txt') as f:
            for i, read in enumerate(f.readlines()):
                seeds = to_seeds(read.decode().strip(), max_mismatch)
                seed_to_orig_seq_idx = defaultdict(set)
                for seed_idx, seed in enumerate(seeds):
                    found_idxes = BurrowsWheelerTransform_Checkpointed.find(
                        bwt_records,
                        bwt_first_indexes_checkpoints,
                        bwt_first_occurrence_map,
                        bwt_last_tallies_checkpoints,
                        seed
                    )
                    for orig_seq_idx in found_idxes:
                        seed_to_orig_seq_idx[seed_idx].add(orig_seq_idx)
                for seed_idx, orig_seq_idxes in seed_to_orig_seq_idx.items():
                    for prev_seed_idx in range(-1, seed_idx - 1, -1):
                        ...  # COMBINE WITH PREV CAPTURED INDEXES
                    for next_seed_idx in range(0, len(seeds)):
                        ...  # COMBINE WITH NEXT CAPTURED INDEXES
                    # TEST NUMBER OF MISMATCHES AGAINST READ HERE
