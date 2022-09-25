`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py) (lines 90 to 101):`{bm-enable-all}`

```python
def get_bwt_first_and_last_columns(
        seq: str,
        end_marker: str
) -> tuple[list[tuple[str, int]], list[tuple[str, int]]]:
    bwt_matrix = to_bwt_matrix(seq, end_marker)
    first = []
    last = []
    for s in bwt_matrix:
        first.append(s[0])
        last.append(s[-1])
    return first, last
```