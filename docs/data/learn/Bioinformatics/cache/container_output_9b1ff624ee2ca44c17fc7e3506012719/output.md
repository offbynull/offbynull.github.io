`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_BacksweepTest.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_BacksweepTest.py) (lines 9 to 31):`{bm-enable-all}`

```python
from sequence_search.BurrowsWheelerTransform_Deserialization import to_bwt_optimized2


def find(
        bwt_array: list[BWTRecord],
        test: str
) -> int:
    top = 0
    bottom = len(bwt_array) - 1
    for ch in reversed(test):
        new_top = len(bwt_array)
        new_bottom = -1
        for i in range(top, bottom + 1):
            record = bwt_array[i]
            if ch == record.last_ch:
                new_top = min(new_top, record.last_to_first_idx)
                new_bottom = max(new_bottom, record.last_to_first_idx)
        if new_bottom == -1 or new_top == len(bwt_array):  # technically only need to check one of these conditions
            return 0
        top = new_top
        bottom = new_bottom
    return (bottom - top) + 1
```