`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_CollapsedFirst.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_CollapsedFirst.py) (lines 12 to 46):`{bm-enable-all}`

```python
class BWTRecord:
    __slots__ = ['last_ch', 'last_ch_cnt']

    def __init__(self, last_ch: str, last_ch_cnt: int):
        self.last_ch = last_ch
        self.last_ch_cnt = last_ch_cnt


def to_bwt_and_first_occurrences(
        seq: str,
        end_marker: str
) -> tuple[list[BWTRecord], dict[str, int]]:
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    seq_rotations = [RotatedStringView(i, seq) for i in range(len(seq))]
    seq_rotations_sorted = sorted(
        seq_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp_char_only(a, b, end_marker))
    )
    prev_first_ch = None
    last_ch_counter = Counter()
    bwt_records = []
    bwt_first_occurrence_map = {}
    for i, s in enumerate(seq_rotations_sorted):
        first_ch = s[0]
        last_ch = s[-1]
        last_ch_counter[last_ch] += 1
        last_ch_cnt = last_ch_counter[last_ch]
        bwt_record = BWTRecord(last_ch, last_ch_cnt)
        bwt_records.append(bwt_record)
        if first_ch != prev_first_ch:
            bwt_first_occurrence_map[first_ch] = i
            prev_first_ch = first_ch
    return bwt_records, bwt_first_occurrence_map
```