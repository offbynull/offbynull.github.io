`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_FirstIndexes.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_FirstIndexes.py) (lines 12 to 51):`{bm-enable-all}`

```python
class BWTRecord:
    __slots__ = ['first_ch', 'first_ch_cnt', 'last_ch', 'last_ch_cnt', 'last_to_first_ptr', 'first_idx']

    def __init__(self, first_ch: str, first_ch_cnt: int, last_ch: str, last_ch_cnt: int, last_to_first_ptr: int, first_idx: int):
        self.first_ch = first_ch
        self.first_ch_cnt = first_ch_cnt
        self.last_ch = last_ch
        self.last_ch_cnt = last_ch_cnt
        self.last_to_first_ptr = last_to_first_ptr
        self.first_idx = first_idx


def to_bwt_with_first_indexes(
        seq: str,
        end_marker: str
) -> list[BWTRecord]:
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    # Create matrix
    seq_with_counts = []
    seq_ch_counter = Counter()
    for ch in seq:
        seq_ch_counter[ch] += 1
        ch_cnt = seq_ch_counter[ch]
        seq_with_counts.append((ch, ch_cnt))
    seq_with_counts_rotations = [(i, RotatedListView(i, seq_with_counts)) for i in range(len(seq_with_counts))]  # rotations + new first_idx for each rotation
    seq_with_counts_rotations_sorted = sorted(
        seq_with_counts_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp(a[1], b[1], end_marker))
    )
    # Create BWT records
    bwt_records = []
    for first_idx, s in seq_with_counts_rotations_sorted:
        first_ch, first_ch_cnt = s[0]
        last_ch, last_ch_cnt = s[-1]
        last_to_first_ptr = next(i for i, (_, row) in enumerate(seq_with_counts_rotations_sorted) if s[-1] == row[0])
        record = BWTRecord(first_ch, first_ch_cnt, last_ch, last_ch_cnt, last_to_first_ptr, first_idx)
        bwt_records.append(record)
    return bwt_records
```