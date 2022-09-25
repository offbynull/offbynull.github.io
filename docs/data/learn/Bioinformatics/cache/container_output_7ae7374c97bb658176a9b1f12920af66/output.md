`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_RanksCheckpointed.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_RanksCheckpointed.py) (lines 151 to 164):`{bm-enable-all}`

```python
def single_tally_to_checkpoint(
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        row: int,
        tally_ch: str
) -> int:
    partial_tally = 0
    while row not in bwt_last_tallies_checkpoints:
        ch = bwt_records[row].last_ch
        if ch == tally_ch:
            partial_tally += 1
        row -= 1
    return partial_tally + bwt_last_tallies_checkpoints[row][tally_ch]
```