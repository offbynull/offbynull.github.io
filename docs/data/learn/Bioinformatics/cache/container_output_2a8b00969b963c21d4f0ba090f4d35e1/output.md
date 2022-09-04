`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py) (lines 13 to 74):`{bm-enable-all}`

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


class BWTRecord:
    __slots__ = ['first_ch', 'first_ch_cnt', 'last_ch', 'last_ch_cnt', 'last_to_first_idx']

    def __init__(self, first_ch: str, first_ch_cnt: int, last_ch: str, last_ch_cnt: int):
        self.first_ch = first_ch
        self.first_ch_cnt = first_ch_cnt
        self.last_ch = last_ch
        self.last_ch_cnt = last_ch_cnt
        self.last_to_first_idx = -1


def to_bwt(
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
    seq_with_counts_rotations = rotate_right(seq_with_counts)
    seq_with_counts_rotations_sorted = sorted(
        seq_with_counts_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp(a, b, end_marker))
    )
    # Pull out first and last columns
    ret = []
    for s in seq_with_counts_rotations_sorted:
        first_ch, first_ch_cnt = s[0]
        last_ch, last_ch_cnt = s[-1]
        record = BWTRecord(first_ch, first_ch_cnt, last_ch, last_ch_cnt)
        ret.append(record)
    # Populate record last-to-first pointers
    for i, record_a in enumerate(ret):
        last = record_a.last_ch, record_a.last_ch_cnt
        for j, record_b in enumerate(ret):
            first = record_b.first_ch, record_b.first_ch_cnt
            if last == first:
                record_a.last_to_first_idx = j
                break
    return ret
```