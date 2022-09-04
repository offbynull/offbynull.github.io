`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py) (lines 134 to 144):`{bm-enable-all}`

```python
def walk(bwt_records: list[BWTRecord]) -> str:
    ret = ''
    row = 0  # first idx of bwt_records always has first_ch == end_marker because of the lexicographical sorting
    while True:
        ret += bwt_records[row].last_ch
        row = bwt_records[row].last_to_first_idx
        if row == 0:
            break
    ret = ret[::-1]  # reverse ret
    ret = ret[1:] + ret[0]  # ret has end_marker at beginning, rotate it to end
    return ret
```