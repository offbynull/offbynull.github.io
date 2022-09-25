`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Ranks.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Ranks.py) (lines 175 to 191):`{bm-enable-all}`

```python
def find(
        bwt_records: list[BWTRecord],
        bwt_first_occurrence_map: dict[str, int],
        test: str
) -> int:
    top = 0
    bottom = len(bwt_records) - 1
    for i, ch in reversed(list(enumerate(test))):
        first_row_for_ch = bwt_first_occurrence_map.get(ch, None)
        if first_row_for_ch is None:  # ch must be in first occurrence map, otherwise it's not in the original seq
            return 0
        top = first_row_for_ch + last_tally_before_row(ch, top, bwt_records)
        bottom = first_row_for_ch + last_tally_at_row(ch, bottom, bwt_records) - 1
        if top > bottom:  # top>bottom once the scan reaches a point in the test sequence where it's not in original seq
            return 0
    return (bottom - top) + 1
```