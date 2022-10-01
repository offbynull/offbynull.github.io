`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_RanksCheckpointed.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_RanksCheckpointed.py) (lines 88 to 99):`{bm-enable-all}`

```python
def walk_tallies_to_checkpoint(
        bwt_records: list[BWTRecord],
        bwt_last_tallies_checkpoints: dict[int, Counter[str]],
        row: int
) -> Counter[str]:
    partial_tallies = Counter()
    while row not in bwt_last_tallies_checkpoints:
        ch = bwt_records[row].last_ch
        partial_tallies[ch] += 1
        row -= 1
    return partial_tallies + bwt_last_tallies_checkpoints[row]
```