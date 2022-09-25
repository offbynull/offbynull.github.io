`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_CollapsedFirst.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_CollapsedFirst.py) (lines 192 to 245):`{bm-enable-all}`

```python
def get_top_bottom_range_for_first(
        bwt_records: list[BWTRecord],
        bwt_first_occurrence_map: dict[str, int],
        ch: str
):
    # End marker will always have been in idx 0 of first
    end_marker = next(first_ch for first_ch, row in bwt_first_occurrence_map.items() if row == 0)
    sorted_keys = sorted(
        bwt_first_occurrence_map.keys(),
        key=functools.cmp_to_key(lambda a, b: cmp_symbol(a, b, end_marker))
    )
    sorted_keys_idx = sorted_keys.index(ch)  # It's possible to replace this with binary search, because keys are sorted
    sorted_keys_next_idx = sorted_keys_idx + 1
    if sorted_keys_next_idx >= len(sorted_keys):
        top = bwt_first_occurrence_map[ch]
        bottom = len(bwt_records) - 1
    else:
        ch_next = sorted_keys[sorted_keys_next_idx]
        top = bwt_first_occurrence_map[ch]
        bottom = bwt_first_occurrence_map[ch_next] - 2
    return top, bottom


def find_optimized(
        bwt_records: list[BWTRecord],
        bwt_first_occurrence_map: dict[str, int],
        test: str
) -> int:
    # Use bwt_first_occurrence_map to determine top&bottom for last char rather than starting off with  a full scan
    top, bottom = get_top_bottom_range_for_first(
        bwt_records,
        bwt_first_occurrence_map,
        test[-1]
    )
    # Since the code above already calculated top&bottom for last char, trim it off before going into the isolation loop
    test = test[:-1]
    for ch in reversed(test):
        new_top = len(bwt_records)
        new_bottom = -1
        for i in range(top, bottom + 1):
            record = bwt_records[i]
            if ch == record.last_ch:
                # last_to_first is now calculated on-the-fly
                last_to_first_idx = to_first_row(
                    bwt_first_occurrence_map,
                    (record.last_ch, record.last_ch_cnt)
                )
                new_top = min(new_top, last_to_first_idx)
                new_bottom = max(new_bottom, last_to_first_idx)
        if new_bottom == -1 or new_top == len(bwt_records):  # technically only need to check one of these conditions
            return 0
        top = new_top
        bottom = new_bottom
    return (bottom - top) + 1
```