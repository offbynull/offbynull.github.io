`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py) (lines 199 to 227):`{bm-enable-all}`

```python
def walk_find(
        first: list[tuple[str, int]],
        last: list[tuple[str, int]],
        test: str,
        start_row: int
) -> bool:
    row = start_row
    for ch in reversed(test[:-1]):
        last_ch, last_ch_cnt = last[row]
        if last_ch != ch:
            return False
        row = next(i for i, (first_ch, first_ch_cnt) in enumerate(first) if first_ch == last_ch and first_ch_cnt == last_ch_cnt)
    return True


def find(
        first: list[tuple[str, int]],
        last: list[tuple[str, int]],
        test: str
) -> int:
    found = 0
    for i, (first_ch, _) in enumerate(first):
        if first_ch == test[-1] and walk_find(first, last, test, i):
            found += 1
    return found
    # The code above is the obvious way to do this. However, since the first column is always sorted by character, the
    # entire array doesn't need to be scanned. Instead, you can binary search to the first and last index with
    # first_ch == test[-1] and just consider those indices.
```