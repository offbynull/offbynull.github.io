`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_FirstIndexes.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_FirstIndexes.py) (lines 100 to 134):`{bm-enable-all}`

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
        row = bwt_records[row].last_to_first_idx
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
    # The code above is the obvious way to do this. However, since the first column is always sorted by character, the
    # entire array doesn't need to be scanned. Instead, you can binary search to the first and last index with
    # rec.first_ch == test[-1] and just consider those indices.
    #
    # The problem with doing this is that bisect_left/bisect_right has a requirement where the binary array being
    # searched must contain the same type as the element being searched for. Even with a custom sorting "key" to try to
    # map between the types on comparison, it won't allow it. See the "standard algorithm" implementation for more info.
```