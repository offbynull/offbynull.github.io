`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Deserialization.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Deserialization.py) (lines 113 to 126):`{bm-enable-all}`

```python
def to_bwt_optimized(
        seq: str,
        end_marker: str
) -> list[BWTRecord]:
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    seq_rotations = rotate_right(seq)
    seq_rotations_sorted = sorted(
        seq_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp_char_only(a[0], b[0], end_marker))
    )
    last_col_seq = ''.join(row[-1] for row in seq_rotations_sorted)
    return to_bwt_from_last_sequence(last_col_seq, end_marker)
```