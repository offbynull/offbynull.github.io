`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py) (lines 11 to 47):`{bm-enable-all}`

```python
def cmp(a: list[tuple[str, int]], b: list[tuple[str, int]], end_marker: str):
    if len(a) != len(b):
        raise '???'
    for (a_ch, _), (b_ch, _) in zip(a, b):
        if a_ch == end_marker and b_ch == end_marker:
            continue
        if a_ch == end_marker:
            return -1
        if b_ch == end_marker:
            return 1
        if a_ch < b_ch:
            return -1
        if a_ch > b_ch:
            return 1
    return 0


def to_bwt_matrix(
        seq: str,
        end_marker: str
) -> list[RotatedListView]:
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    # Create matrix
    seq_with_counts = []
    seq_ch_counter = Counter()
    for ch in seq:
        seq_ch_counter[ch] += 1
        ch_cnt = seq_ch_counter[ch]
        seq_with_counts.append((ch, ch_cnt))
    seq_with_counts_rotations = [RotatedListView(i, seq_with_counts) for i in range(len(seq_with_counts))]
    seq_with_counts_rotations_sorted = sorted(
        seq_with_counts_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp(a, b, end_marker))
    )
    return seq_with_counts_rotations_sorted
```