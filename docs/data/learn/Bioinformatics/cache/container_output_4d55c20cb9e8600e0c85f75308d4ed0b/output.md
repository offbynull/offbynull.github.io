`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_FirstIndexesCheckpointed.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_FirstIndexesCheckpointed.py) (lines 12 to 61):`{bm-enable-all}`

```python
class BWTRecord:
    __slots__ = ['first_ch', 'first_ch_cnt', 'last_ch', 'last_ch_cnt', 'last_to_first_idx']

    def __init__(self, first_ch: str, first_ch_cnt: int, last_ch: str, last_ch_cnt: int):
        self.first_ch = first_ch
        self.first_ch_cnt = first_ch_cnt
        self.last_ch = last_ch
        self.last_ch_cnt = last_ch_cnt
        self.last_to_first_idx = -1


def to_bwt_with_first_indexes_checkpointed(
        seq: str,
        end_marker: str,
        first_indexes_checkpoint_n: int
) -> tuple[list[BWTRecord], dict[int, int]]:
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
    # Pull out first and last columns
    bwt_records = []
    bwt_first_indexes_checkpoints = {}
    for i, (first_idx, s) in enumerate(seq_with_counts_rotations_sorted):
        first_ch, first_ch_cnt = s[0]
        last_ch, last_ch_cnt = s[-1]
        record = BWTRecord(first_ch, first_ch_cnt, last_ch, last_ch_cnt)
        bwt_records.append(record)
        if first_idx % first_indexes_checkpoint_n == 0:
            bwt_first_indexes_checkpoints[i] = first_idx
    # Populate record last-to-first pointers
    for i, record_a in enumerate(bwt_records):
        last = record_a.last_ch, record_a.last_ch_cnt
        for j, record_b in enumerate(bwt_records):
            first = record_b.first_ch, record_b.first_ch_cnt
            if last == first:
                record_a.last_to_first_idx = j
                break
    return bwt_records, bwt_first_indexes_checkpoints
```