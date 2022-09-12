`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Ranks.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Ranks.py) (lines 121 to 159):`{bm-enable-all}`

```python
def compute_new_top(
        ch: str,
        top: int,
        first_occurrence_idx_for_ch: int,
        bwt_records: list[BWTRecord]
):
    incremented_at_top = bwt_records[top].last_ch == ch
    offset = 0
    if incremented_at_top:
        offset = 1
    return first_occurrence_idx_for_ch + (bwt_records[top].last_tallies[ch] - offset)


def compute_new_bottom(
        ch: str,
        bottom: int,
        first_occurrence_idx_for_ch: int,
        bwt_records: list[BWTRecord]
):
    return first_occurrence_idx_for_ch + (bwt_records[bottom].last_tallies[ch] - 1)


def find(
        bwt_records: list[BWTRecord],
        bwt_first_occurrence_map: dict[str, int],
        test: str
) -> int:
    top = 0
    bottom = len(bwt_records) - 1
    for i, ch in reversed(list(enumerate(test))):
        first_idx_for_ch = bwt_first_occurrence_map.get(ch, None)
        if first_idx_for_ch is None:  # ch must be in first occurrence map, otherwise it's not in the original seq
            return 0
        top = compute_new_top(ch, top, first_idx_for_ch, bwt_records)
        bottom = compute_new_bottom(ch, bottom, first_idx_for_ch, bwt_records)
        if top > bottom:  # top>bottom once the scan reaches a point in the test sequence where it's not in original seq
            return 0
    return (bottom - top) + 1
```