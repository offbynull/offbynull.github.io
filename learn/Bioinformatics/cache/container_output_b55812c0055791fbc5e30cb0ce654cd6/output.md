`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py) (lines 139 to 153):`{bm-enable-all}`

```python
def walk(
        first: list[tuple[str, int]],
        last: list[tuple[str, int]]
) -> str:
    ret = ''
    row = 0  # first idx always has first_ch == end_marker because of the lexicographical sorting
    end_marker, _ = first[row]
    while True:
        last_ch, last_ch_cnt = last[row]
        if last_ch == end_marker:
            break
        ret += last_ch
        row = next(i for i, (first_ch, first_ch_cnt) in enumerate(first) if first_ch == last_ch and first_ch_cnt == last_ch_cnt)
    ret = ret[::-1] + end_marker  # reverse ret and add end marker
    return ret
```