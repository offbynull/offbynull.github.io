`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_RanksCheckpointed.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_RanksCheckpointed.py) (lines 94 to 105):`{bm-enable-all}`

```python
def walk_tallies_to_checkpoint(
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        idx: int
) -> Counter[str]:
    partial_tallies = Counter()
    while idx not in bwt_last_tallies_checkpoints:
        ch = bwt_records[idx].last_ch
        partial_tallies[ch] += 1
        idx -= 1
    return partial_tallies + bwt_last_tallies_checkpoints[idx]
```