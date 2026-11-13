`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Deserialization.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Deserialization.py) (lines 212 to 249):`{bm-enable-all}`

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
        key=functools.cmp_to_key(lambda a, b: cmp_symbol(a, b, end_marker))
    )
    first_ch_counter = Counter()
    last_ch_counter = Counter()
    first = []
    last = []
    bwt_records = []
    for i, s in enumerate(seq_rotations_sorted):
        first_ch = s[0]
        first_ch_counter[first_ch] += 1
        first_ch_cnt = first_ch_counter[first_ch]
        last_ch = s[-1]
        last_ch_counter[last_ch] += 1
        last_ch_cnt = last_ch_counter[last_ch]
        first.append((first_ch, first_ch_cnt))
        last.append((last_ch, last_ch_cnt))
    for (first_ch, first_ch_cnt), (last_ch, last_ch_cnt) in zip(first, last):
        # Create record
        rec = BWTRecord(first_ch, first_ch_cnt, last_ch, last_ch_cnt, -1)
        # Figure out where in first that (last_ch, last_ch_cnt) occurs using binary search. This is
        # possible because first is sorted.
        rec.last_to_first_ptr = bisect_left(
            FirstColBisectableWrapper(first, end_marker),
            (last_ch, last_ch_cnt)
        )
        # Append to return
        bwt_records.append(rec)
    return bwt_records
```