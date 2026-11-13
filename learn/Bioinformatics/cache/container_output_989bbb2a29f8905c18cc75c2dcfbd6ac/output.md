`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Ranks.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Ranks.py) (lines 188 to 206):`{bm-enable-all}`

```python
def find(
        bwt_records: list[BWTRecord],
        bwt_first_occurrence_map: dict[str, int],
        test: str
) -> int:
    top_row = 0
    bottom_row = len(bwt_records) - 1
    for i, ch in reversed(list(enumerate(test))):
        first_row_for_ch = bwt_first_occurrence_map.get(ch, None)
        if first_row_for_ch is None:  # ch must be in first occurrence map, otherwise it's not in the original seq
            return 0
        top_symbol_instance = ch, last_tally_before_row(ch, top_row, bwt_records) + 1
        top_row = last_to_first(bwt_first_occurrence_map, top_symbol_instance)
        bottom_symbol_instance = ch, last_tally_at_row(ch, bottom_row, bwt_records)
        bottom_row = last_to_first(bwt_first_occurrence_map, bottom_symbol_instance)
        if top_row > bottom_row:  # top>bottom once the scan reaches a point in the test sequence where it's not in original seq
            return 0
    return (bottom_row - top_row) + 1
```