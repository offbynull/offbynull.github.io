`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic_LastToFirst.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic_LastToFirst.py) (lines 11 to 38):`{bm-enable-all}`

```python
class BWTRecord:
    __slots__ = ['first_ch', 'first_ch_cnt', 'last_ch', 'last_ch_cnt', 'last_to_first_idx']

    def __init__(self, first_ch: str, first_ch_cnt: int, last_ch: str, last_ch_cnt: int, last_to_first_idx: int):
        self.first_ch = first_ch
        self.first_ch_cnt = first_ch_cnt
        self.last_ch = last_ch
        self.last_ch_cnt = last_ch_cnt
        self.last_to_first_idx = last_to_first_idx


def to_bwt_records(
        seq: str,
        end_marker: str
) -> list[BWTRecord]:
    first, last = BurrowsWheelerTransform_Basic.get_bwt_first_and_last_columns(seq, end_marker)
    # Create cache of last-to-first pointers
    last_to_first = []
    for last_val in last:
        idx = next(i for i, first_val in enumerate(first) if last_val == first_val)
        last_to_first.append(idx)
    # Create records
    bwt_records = []
    for (first_ch, first_ch_cnt), (last_ch, last_ch_cnt), last_to_first_idx in zip(first, last, last_to_first):
        bwt_records.append(BWTRecord(first_ch, first_ch_cnt, last_ch, last_ch_cnt, last_to_first_idx))
    # Return
    return bwt_records
```