`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Checkpointed.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Checkpointed.py) (lines 255 to 309):`{bm-enable-all}`

```python
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
    top_row = 0
    bottom_row = len(bwt_records) - 1
    for i, ch in reversed(list(enumerate(test))):
        first_row_for_ch = bwt_first_occurrence_map.get(ch, None)
        if first_row_for_ch is None:  # ch must be in first occurrence map, otherwise it's not in the original seq
            return []
        top_symbol_instance = ch, last_tally_before_row(ch, top_row, bwt_records, bwt_last_tallies_checkpoints) + 1
        top_row = last_to_first(bwt_first_occurrence_map, top_symbol_instance)
        bottom_symbol_instance = ch, last_tally_at_row(ch, bottom_row, bwt_records, bwt_last_tallies_checkpoints)
        bottom_row = last_to_first(bwt_first_occurrence_map, bottom_symbol_instance)
        if top_row > bottom_row:  # top>bottom once the scan reaches a point in the test sequence where it's not in original seq
            return []
    # Find first_index for each entry in between top and bottom
    first_idxes = []
    for index in range(top_row, bottom_row + 1):
        first_idx = walk_back_until_first_indexes_checkpoint(
            bwt_records,
            bwt_first_indexes_checkpoints,
            bwt_first_occurrence_map,
            bwt_last_tallies_checkpoints,
            index
        )
        first_idxes.append(first_idx)
    return first_idxes
```