`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Checkpointed.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Checkpointed.py) (lines 134 to 165):`{bm-enable-all}`

```python
def walk_back_until_first_index_checkpoint(
        bwt_records: list[BWTRecord],
        bwt_first_indexes_checkpoints: dict[int, int],
        bwt_first_occurrence_map: dict[str, int],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        row: int
) -> int:
    walk_cnt = 0
    while row not in bwt_first_indexes_checkpoints:
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
        last_ch = bwt_records[row].last_ch
        last_ch_cnt = to_last_symbol_instance_count(bwt_records, bwt_last_tallies_checkpoints, row)
        row = last_to_first(bwt_first_occurrence_map, (last_ch, last_ch_cnt))
        walk_cnt += 1
    first_idx = bwt_first_indexes_checkpoints[row] + walk_cnt
    # It's possible that the walk back continues backward before the start of the sequence, resulting
    # in it looping to the end and continuing to walk back from there. If that happens, the code below
    # adjusts it.
    sequence_len = len(bwt_records)
    if first_idx >= sequence_len:
        first_idx -= sequence_len
    return first_idx
```