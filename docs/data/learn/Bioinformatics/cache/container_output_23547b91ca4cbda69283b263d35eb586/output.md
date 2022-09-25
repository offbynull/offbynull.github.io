`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_BacksweepTest.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_BacksweepTest.py) (lines 10 to 37):`{bm-enable-all}`

```python
def find(
        bwt_records: list[BWTRecord],
        test: str
) -> int:
    top = 0
    bottom = len(bwt_records) - 1
    for ch in reversed(test):
        # Scan down to find new top, which is the first instance of ch (lowest symbol instance count for ch)
        new_top = len(bwt_records)
        for i in range(top, bottom + 1):
            record = bwt_records[i]
            if ch == record.last_ch:
                new_top = record.last_to_first_ptr
                break
        # Scan up to find new bottom, which is the last instance of ch (highest symbol instance count for ch)
        new_bottom = -1
        for i in range(bottom, top - 1, -1):
            record = bwt_records[i]
            if ch == record.last_ch:
                new_bottom = record.last_to_first_ptr
                break
        # Check if not found
        if new_bottom == -1 or new_top == len(bwt_records):  # technically only need to check one of these conditions
            return 0
        top = new_top
        bottom = new_bottom
    return (bottom - top) + 1
```