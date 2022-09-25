`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_FirstIndexesCheckpointed.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_FirstIndexesCheckpointed.py) (lines 9 to 34):`{bm-enable-all}`

```python
class BWTRecord:
    __slots__ = ['first_ch', 'first_ch_cnt', 'last_ch', 'last_ch_cnt', 'last_to_first_ptr']

    def __init__(self, first_ch: str, first_ch_cnt: int, last_ch: str, last_ch_cnt: int, last_to_first_ptr: int):
        self.first_ch = first_ch
        self.first_ch_cnt = first_ch_cnt
        self.last_ch = last_ch
        self.last_ch_cnt = last_ch_cnt
        self.last_to_first_ptr = last_to_first_ptr


def to_bwt_with_first_indexes_checkpointed(
        seq: str,
        end_marker: str,
        first_indexes_checkpoint_n: int
) -> tuple[list[BWTRecord], dict[int, int]]:
    full_bwt_records = BurrowsWheelerTransform_FirstIndexes.to_bwt_with_first_indexes(seq, end_marker)
    bwt_records = []
    bwt_first_indexes_checkpoints = {}
    for i, rec in enumerate(full_bwt_records):
        if rec.first_idx % first_indexes_checkpoint_n == 0:
            bwt_first_indexes_checkpoints[i] = rec.first_idx
        new_rec = BWTRecord(rec.first_ch, rec.first_ch_cnt, rec.last_ch, rec.last_ch_cnt, rec.last_to_first_ptr)
        bwt_records.append(new_rec)
    return bwt_records, bwt_first_indexes_checkpoints
```