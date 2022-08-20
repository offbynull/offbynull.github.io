`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Deserialization.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Deserialization.py) (lines 13 to 70):`{bm-enable-all}`

```python
from sequence_search.BurrowsWheelerTransform_Basic import BWTRecord, walk


def cmp_char_only(a: str, b: str, end_marker: str):
    if len(a) != len(b):
        raise '???'
    for a_ch, b_ch in zip(a, b):
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


def cmp_char_and_instance(a: tuple[str, int], b: tuple[str, int], end_marker: str):
    # compare symbol
    x = cmp_char_only(a[0], b[0], end_marker)
    if x != 0:
        return x
    # compare symbol instance count
    if a[1] < b[1]:
        return -1
    elif a[1] > b[1]:
        return 1
    return 0


def to_bwt_from_last_sequence(
        last_col_seq: str,
        end_marker: str
) -> list[BWTRecord]:
    # Create first and last columns
    ret = []
    last_ch_counter = Counter()
    last_col = []
    for last_ch in last_col_seq:
        last_ch_counter[last_ch] += 1
        last_ch_count = last_ch_counter[last_ch]
        last_col.append((last_ch, last_ch_count))
    first_col = sorted(last_col, key=functools.cmp_to_key(lambda a, b: cmp_char_and_instance(a, b, end_marker)))
    for (first_ch, first_ch_idx), (last_ch, last_ch_idx) in zip(first_col, last_col):
        record = BWTRecord(first_ch, first_ch_idx, last_ch, last_ch_idx)
        ret.append(record)
    # Populate record last-to-first pointers
    for i, record_a in enumerate(ret):
        last = record_a.last_ch, record_a.last_ch_idx
        for j, record_b in enumerate(ret):
            first = record_b.first_ch, record_b.first_ch_idx
            if last == first:
                record_a.last_to_first_idx = j
                break
    return ret
```