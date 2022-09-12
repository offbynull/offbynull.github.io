`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Checkpointed.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Checkpointed.py) (lines 259 to 314):`{bm-enable-all}`

```python
def compute_new_top(
        ch: str,
        top: int,
        first_occurrence_idx_for_ch: int,
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]]
):
    incremented_at_top = bwt_records[top].last_ch == ch
    offset = 0
    if incremented_at_top:
        offset = 1
    last_tally_for_ch_top = single_tally_to_checkpoint(bwt_records, bwt_last_tallies_checkpoints, top, ch)
    return first_occurrence_idx_for_ch + (last_tally_for_ch_top - offset)


def compute_new_bottom(
        ch: str,
        bottom: int,
        first_occurrence_idx_for_ch: int,
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]]
):
    last_tally_for_ch_bottom = single_tally_to_checkpoint(bwt_records, bwt_last_tallies_checkpoints, bottom, ch)
    return first_occurrence_idx_for_ch + (last_tally_for_ch_bottom - 1)


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
        top = compute_new_top(ch, top, first_idx_for_ch, bwt_records, bwt_last_tallies_checkpoints)
        bottom = compute_new_bottom(ch, bottom, first_idx_for_ch, bwt_records, bwt_last_tallies_checkpoints)
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