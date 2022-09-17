`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Ranks.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Ranks.py) (lines 121 to 139):`{bm-enable-all}`

```python
def symbol_tally_at_index(
        symbol: str,
        idx: int,
        bwt_records: list[BWTRecord]
):
    ch_tally = bwt_records[idx].last_tallies[symbol]
    return ch_tally


def symbol_tally_before_index(
        symbol: str,
        idx: int,
        bwt_records: list[BWTRecord]
):
    ch_incremented_at_idx = bwt_records[idx].last_ch == symbol
    ch_tally = bwt_records[idx].last_tallies[symbol]
    if ch_incremented_at_idx:
        ch_tally -= 1
    return ch_tally
```