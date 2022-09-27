`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_CollapsedFirst.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_CollapsedFirst.py) (lines 140 to 165):`{bm-enable-all}`

```python
def find(
        bwt_records: list[BWTRecord],
        bwt_first_occurrence_map: dict[str, int],
        test: str
) -> int:
    top = 0
    bottom = len(bwt_records) - 1
    for ch in reversed(test):
        new_top = len(bwt_records)
        new_bottom = -1
        for i in range(top, bottom + 1):
            record = bwt_records[i]
            if ch == record.last_ch:
                # last_to_first is now calculated on-the-fly
                last_to_first_ptr = last_to_first(
                    bwt_first_occurrence_map,
                    (record.last_ch, record.last_ch_cnt)
                )
                new_top = min(new_top, last_to_first_ptr)
                new_bottom = max(new_bottom, last_to_first_ptr)
        if new_bottom == -1 or new_top == len(bwt_records):  # technically only need to check one of these conditions
            return 0
        top = new_top
        bottom = new_bottom
    return (bottom - top) + 1
```