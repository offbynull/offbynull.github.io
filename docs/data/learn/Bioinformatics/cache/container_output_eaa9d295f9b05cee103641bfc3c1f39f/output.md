`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_FirstIndexes.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_FirstIndexes.py) (lines 94 to 121):`{bm-enable-all}`

```python
def walk_find(
        bwt_records: list[BWTRecord],
        test: str,
        start_row: int
) -> int | None:
    row = start_row
    for ch in reversed(test[:-1]):
        if bwt_records[row].last_ch != ch:
            return None
        row = bwt_records[row].last_to_first_ptr
    return bwt_records[row].first_idx


def find(
        bwt_records: list[BWTRecord],
        test: str
) -> list[int]:
    found = []
    for i, rec in enumerate(bwt_records):
        if rec.first_ch == test[-1]:
            if len(test) == 1:
                found.append(rec.first_idx)
            elif rec.last_ch == test[-2]:
                found_idx = walk_find(bwt_records, test, i)
                if found_idx is not None:
                    found.append(found_idx)
    return found
```