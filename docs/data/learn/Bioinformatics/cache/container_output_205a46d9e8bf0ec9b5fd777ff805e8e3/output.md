`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Ranks.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Ranks.py) (lines 116 to 134):`{bm-enable-all}`

```python
def last_tally_at_row(
        symbol: str,
        row: int,
        bwt_records: list[BWTRecord]
):
    ch_tally = bwt_records[row].last_tallies[symbol]
    return ch_tally


def last_tally_before_row(
        symbol: str,
        row: int,
        bwt_records: list[BWTRecord]
):
    ch_incremented_at_row = bwt_records[row].last_ch == symbol
    ch_tally = bwt_records[row].last_tallies[symbol]
    if ch_incremented_at_row:
        ch_tally -= 1
    return ch_tally
```