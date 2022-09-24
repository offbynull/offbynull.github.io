`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic_LastToFirst.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic_LastToFirst.py) (lines 80 to 115):`{bm-enable-all}`

```python
def walk(bwt_records: list[BWTRecord]) -> str:
    ret = ''
    row = 0  # first idx always has first_ch == end_marker because of the lexicographical sorting
    while True:
        ret += bwt_records[row].last_ch
        row = bwt_records[row].last_to_first_idx
        if row == 0:
            break
    ret = ret[::-1]  # reverse ret
    ret = ret[1:] + ret[0]  # ret has end_marker at beginning, rotate it to end
    return ret


def walk_find(
        bwt_records: list[BWTRecord],
        test: str,
        start_row: int
) -> bool:
    row = start_row
    for ch in reversed(test[:-1]):
        if bwt_records[row].last_ch != ch:
            return False
        row = bwt_records[row].last_to_first_idx
    return True


def find(
        bwt_records: list[BWTRecord],
        test: str
) -> int:
    found = 0
    for i, rec in enumerate(bwt_records):
        if rec.first_ch == test[-1]:
            if len(test) == 1 or (rec.last_ch == test[-2] and walk_find(bwt_records, test, i)):
                found += 1
    return found
```