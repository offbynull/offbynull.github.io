`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_RanksCheckpointed.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_RanksCheckpointed.py) (lines 213 to 272):`{bm-enable-all}`

```python
def to_last_symbol_instance_count(
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        idx: int
) -> int:
    return single_tally_to_checkpoint(bwt_records, bwt_last_tallies_checkpoints, idx, bwt_records[idx].last_ch)


def to_first_index(
        bwt_first_occurrence_map: dict[str, int],
        symbol_instance: tuple[str, int]
) -> int:
    symbol, symbol_count = symbol_instance
    return bwt_first_occurrence_map[symbol] + symbol_count - 1


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
        bwt_first_occurrence_map: dict[str, int],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        test: str
) -> int:
    top = 0
    bottom = len(bwt_records) - 1
    for i, ch in reversed(list(enumerate(test))):
        first_idx_for_ch = bwt_first_occurrence_map.get(ch, None)
        if first_idx_for_ch is None:  # ch must be in first occurrence map, otherwise it's not in the original seq
            return 0
        top = compute_new_top(ch, top, first_idx_for_ch, bwt_records, bwt_last_tallies_checkpoints)
        bottom = compute_new_bottom(ch, bottom, first_idx_for_ch, bwt_records, bwt_last_tallies_checkpoints)
        if top > bottom:  # top>bottom once the scan reaches a point in the test sequence where it's not in original seq
            return 0
    return (bottom - top) + 1
```