`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py) (lines 139 to 153):`{bm-enable-all}`

```python
def walk(
        first: list[tuple[str, int]],
        last: list[tuple[str, int]]
) -> str:
    ret = ''
    row = 0  # first idx always has first_ch == end_marker because of the lexicographical sorting
    while True:
        last_ch, last_ch_cnt = last[row]
        ret += last_ch
        row = next(i for i, (first_ch, first_ch_cnt) in enumerate(first) if first_ch == last_ch and first_ch_cnt == last_ch_cnt)
        if row == 0:
            break
    ret = ret[::-1]  # reverse ret
    ret = ret[1:] + ret[0]  # ret has end_marker at beginning, rotate it to end
    return ret
```