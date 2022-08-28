`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_RanksCheckpointed.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_RanksCheckpointed.py) (lines 153 to 166):`{bm-enable-all}`

```python
def single_tally_to_checkpoint(
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        idx: int
) -> int:
    tally_ch = bwt_records[idx].last_ch
    partial_tally = 0
    while idx not in bwt_last_tallies_checkpoints:
        ch = bwt_records[idx].last_ch
        if ch == tally_ch:
            partial_tally += 1
        idx -= 1
    return partial_tally + bwt_last_tallies_checkpoints[idx][tally_ch]
```