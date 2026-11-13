`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Deserialization.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Deserialization.py) (lines 45 to 99):`{bm-enable-all}`

```python
def cmp_symbol(a: str, b: str, end_marker: str):
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


def cmp_symbol_and_count(a: tuple[str, int], b: tuple[str, int], end_marker: str):
    # compare symbol
    x = cmp_symbol(a[0], b[0], end_marker)
    if x != 0:
        return x
    # compare symbol instance count
    if a[1] < b[1]:
        return -1
    elif a[1] > b[1]:
        return 1
    return 0


def to_bwt_from_last_sequence(
        last_seq: str,
        end_marker: str
) -> list[BWTRecord]:
    # Create first and last columns
    bwt_records = []
    last_ch_counter = Counter()
    last = []
    for last_ch in last_seq:
        last_ch_counter[last_ch] += 1
        last_ch_count = last_ch_counter[last_ch]
        last.append((last_ch, last_ch_count))
    first = sorted(last, key=functools.cmp_to_key(lambda a, b: cmp_symbol_and_count(a, b, end_marker)))
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