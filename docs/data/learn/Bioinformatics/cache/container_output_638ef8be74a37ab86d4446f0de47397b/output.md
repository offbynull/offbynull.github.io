`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Checkpointed.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Checkpointed.py) (lines 364 to 500):`{bm-enable-all}`

```python
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
#     bwt_records = BurrowsWheelerTransform_Deserialization.to_bwt_from_last_sequence(last_col, '$')
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
                    extraction_bwt_idx = len(bwt_records) - 1
                else:
                    extraction_bwt_idx = first_index_to_bwt_row[test_seq_end_idx_moved_up_to_first_idxes_checkpoint]
                extraction_len = test_seq_end_idx_moved_up_to_first_idxes_checkpoint - test_seq_start_idx
                extracted_test_seq_segment = walk_back_and_extract(
                    bwt_records,
                    bwt_first_occurrence_map,
                    bwt_last_tallies_checkpoints,
                    extraction_bwt_idx,
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
        index: int,
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
        ret += bwt_records[index].last_ch
        last_ch = bwt_records[index].last_ch
        last_ch_cnt = to_last_symbol_instance_count(bwt_records, bwt_last_tallies_checkpoints, index)
        index = to_first_index(bwt_first_occurrence_map, (last_ch, last_ch_cnt))
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
```