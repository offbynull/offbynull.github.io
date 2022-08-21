`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_SquashedFirst.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_SquashedFirst.py) (lines 14 to 54):`{bm-enable-all}`

```python
class BWTRecord:
    __slots__ = ['last_ch', 'last_ch_idx']

    def __init__(self, last_ch: str, last_ch_idx: int):
        self.last_ch = last_ch
        self.last_ch_idx = last_ch_idx

    def __str__(self):
        return f'{self.last_ch}{self.last_ch_idx}'

    def __repr__(self):
        return str(self)


def to_bwt_and_first_occurrences(
        seq: str,
        end_marker: str
) -> tuple[list[BWTRecord], dict[str, int]]:
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    seq_rotations = rotate_right(seq)
    seq_rotations_sorted = sorted(
        seq_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp_char_only(a, b, end_marker))
    )
    prev_first_ch = None
    last_ch_counter = Counter()
    bwt_array = []
    bwt_first_occurrence_map = {}
    for i, s in enumerate(seq_rotations_sorted):
        first_ch = s[0]
        last_ch = s[-1]
        last_ch_counter[last_ch] += 1
        last_ch_idx = last_ch_counter[last_ch]
        bwt_record = BWTRecord(last_ch, last_ch_idx)
        bwt_array.append(bwt_record)
        if first_ch != prev_first_ch:
            bwt_first_occurrence_map[first_ch] = i
            prev_first_ch = first_ch
    return bwt_array, bwt_first_occurrence_map
```