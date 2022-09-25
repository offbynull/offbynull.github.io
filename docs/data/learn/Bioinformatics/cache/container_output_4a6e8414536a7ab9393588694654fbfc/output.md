`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_RanksCheckpointed.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_RanksCheckpointed.py) (lines 213 to 269):`{bm-enable-all}`

```python
def to_last_symbol_instance_count(
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        row: int
) -> int:
    return single_tally_to_checkpoint(bwt_records, bwt_last_tallies_checkpoints, row, bwt_records[row].last_ch)


def to_first_index(
        bwt_first_occurrence_map: dict[str, int],
        symbol_instance: tuple[str, int]
) -> int:
    symbol, symbol_count = symbol_instance
    return bwt_first_occurrence_map[symbol] + symbol_count - 1


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
        bwt_first_occurrence_map: dict[str, int],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        test: str
) -> int:
    top = 0
    bottom = len(bwt_records) - 1
    for i, ch in reversed(list(enumerate(test))):
        first_row_for_ch = bwt_first_occurrence_map.get(ch, None)
        if first_row_for_ch is None:  # ch must be in first occurrence map, otherwise it's not in the original seq
            return 0
        top = first_row_for_ch + last_tally_before_row(ch, top, bwt_records, bwt_last_tallies_checkpoints)
        bottom = first_row_for_ch + last_tally_at_row(ch, bottom, bwt_records, bwt_last_tallies_checkpoints) - 1
        if top > bottom:  # top>bottom once the scan reaches a point in the test sequence where it's not in original seq
            return 0
    return (bottom - top) + 1
```