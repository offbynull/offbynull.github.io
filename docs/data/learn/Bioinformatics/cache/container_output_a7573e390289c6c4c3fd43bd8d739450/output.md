`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Checkpointed.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Checkpointed.py) (lines 259 to 311):`{bm-enable-all}`

```python
def symbol_tally_before_index(
        symbol: str,
        idx: int,
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]]
):
    ch_incremented_at_idx = bwt_records[idx].last_ch == symbol
    ch_tally = single_tally_to_checkpoint(bwt_records, bwt_last_tallies_checkpoints, idx, symbol)
    if ch_incremented_at_idx:
        ch_tally -= 1
    return ch_tally


def symbol_tally_at_index(
        symbol: str,
        idx: int,
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]]
):
    ch_tally = single_tally_to_checkpoint(bwt_records, bwt_last_tallies_checkpoints, idx, symbol)
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
        first_idx_for_ch = bwt_first_occurrence_map.get(ch, None)
        if first_idx_for_ch is None:  # ch must be in first occurrence map, otherwise it's not in the original seq
            return []
        top = first_idx_for_ch + symbol_tally_before_index(ch, top, bwt_records, bwt_last_tallies_checkpoints)
        bottom = first_idx_for_ch + symbol_tally_at_index(ch, bottom, bwt_records, bwt_last_tallies_checkpoints) - 1
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
```