`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic_LastToFirst.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic_LastToFirst.py) (lines 80 to 116):`{bm-enable-all}`

```python
def walk(bwt_records: list[BWTRecord]) -> str:
    ret = ''
    row = 0  # first idx always has first_ch == end_marker because of the lexicographical sorting
    end_marker = bwt_records[row].first_ch
    while True:
        last_ch = bwt_records[row].last_ch
        if last_ch == end_marker:
            break
        ret += last_ch
        row = bwt_records[row].last_to_first_ptr
    ret = ret[::-1] + end_marker  # reverse ret and add end marker
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
        row = bwt_records[row].last_to_first_ptr
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