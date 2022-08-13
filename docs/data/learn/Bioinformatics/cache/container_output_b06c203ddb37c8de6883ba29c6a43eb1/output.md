`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py) (lines 248 to 272):`{bm-enable-all}`

```python
def walk_find(
        bwt_array: list[BWTRecord],
        test: str,
        start_row: int
) -> bool:
    if bwt_array[start_row].last_ch != test[0]:
        raise ValueError('First character must match start row\'s last column value')
    row = start_row
    for ch in test:
        if bwt_array[row].last_ch != ch:
            return False
        row = bwt_array[row].last_to_first_idx
    return True


def find(
        bwt_array: list[BWTRecord],
        test: str
) -> int:
    found = 0
    for i, rec in enumerate(bwt_array):
        if rec.last_ch == test[0] and walk_find(bwt_array, test, i):
            found += 1
    return found
```