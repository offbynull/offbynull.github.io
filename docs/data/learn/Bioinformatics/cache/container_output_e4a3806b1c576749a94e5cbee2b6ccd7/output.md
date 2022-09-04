`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_FirstIndexes.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_FirstIndexes.py) (lines 13 to 59):`{bm-enable-all}`

```python
class BWTRecord:
    __slots__ = ['first_ch', 'first_ch_cnt', 'last_ch', 'last_ch_cnt', 'last_to_first_idx', 'first_idx']

    def __init__(self, first_ch: str, first_ch_cnt: int, last_ch: str, last_ch_cnt: int, first_idx: int):
        self.first_ch = first_ch
        self.first_ch_cnt = first_ch_cnt
        self.last_ch = last_ch
        self.last_ch_cnt = last_ch_cnt
        self.last_to_first_idx = -1
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
    seq_with_counts_rotations = rotate_right_with_shift_counts(seq_with_counts)  # rotations + new first_idx for each rotation
    seq_with_counts_rotations_sorted = sorted(
        seq_with_counts_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp(a[1], b[1], end_marker))
    )
    # Pull out first and last columns
    bwt_records = []
    for first_idx, s in seq_with_counts_rotations_sorted:
        first_ch, first_ch_cnt = s[0]
        last_ch, last_ch_cnt = s[-1]
        record = BWTRecord(first_ch, first_ch_cnt, last_ch, last_ch_cnt, first_idx)
        bwt_records.append(record)
    # Populate record last-to-first pointers
    for i, record_a in enumerate(bwt_records):
        last = record_a.last_ch, record_a.last_ch_cnt
        for j, record_b in enumerate(bwt_records):
            first = record_b.first_ch, record_b.first_ch_cnt
            if last == first:
                record_a.last_to_first_idx = j
                break
    return bwt_records
```