`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Deserialization.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Deserialization.py) (lines 211 to 249):`{bm-enable-all}`

```python
def to_bwt_optimized2(
        seq: str,
        end_marker: str
) -> list[BWTRecord]:
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    # Create first and last columns
    seq_rotations = [RotatedStringView(i, seq) for i in range(len(seq))]
    seq_rotations_sorted = sorted(
        seq_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp_char_only(a, b, end_marker))
    )
    first_ch_counter = Counter()
    last_ch_counter = Counter()
    first_col = []
    last_col = []
    ret = []
    for i, s in enumerate(seq_rotations_sorted):
        first_ch = s[0]
        first_ch_counter[first_ch] += 1
        first_ch_cnt = first_ch_counter[first_ch]
        last_ch = s[-1]
        last_ch_counter[last_ch] += 1
        last_ch_cnt = last_ch_counter[last_ch]
        first_col.append((first_ch, first_ch_cnt))
        last_col.append((last_ch, last_ch_cnt))
    for (first_ch, first_ch_cnt), (last_ch, last_ch_cnt) in zip(first_col, last_col):
        # Create record
        record = BWTRecord(first_ch, first_ch_cnt, last_ch, last_ch_cnt, -1)
        # Figure out where in first_col that (last_ch, last_ch_cnt) occurs using binary search. This is
        # possible because first_col is sorted.
        first_col_idx = bisect_left(
            FirstColBisectableWrapper(first_col, end_marker),
            (last_ch, last_ch_cnt)
        )
        record.last_to_first_idx = first_col_idx
        # Append to return
        ret.append(record)
    return ret
```