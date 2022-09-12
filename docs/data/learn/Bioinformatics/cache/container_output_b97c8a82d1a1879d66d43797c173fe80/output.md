`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_RanksCheckpointed.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_RanksCheckpointed.py) (lines 12 to 48):`{bm-enable-all}`

```python
class BWTRecord:
    __slots__ = ['last_ch']

    def __init__(self, last_ch: str):
        self.last_ch = last_ch


def to_bwt_ranked_checkpointed(
        seq: str,
        end_marker: str,
        last_tallies_checkpoint_n: int
) -> tuple[list[BWTRecord], dict[str, int], dict[int, Counter[str]]]:
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
    bwt_last_tallies_checkpoints = {}
    for i, s in enumerate(seq_rotations_sorted):
        first_ch = s[0]
        last_ch = s[-1]
        last_ch_counter[last_ch] += 1
        bwt_record = BWTRecord(last_ch)
        bwt_records.append(bwt_record)
        if i % last_tallies_checkpoint_n == 0:
            bwt_last_tallies_checkpoints[i] = last_ch_counter.copy()
        if first_ch != prev_first_ch:
            bwt_first_occurrence_map[first_ch] = i
            prev_first_ch = first_ch
    return bwt_records, bwt_first_occurrence_map, bwt_last_tallies_checkpoints
```