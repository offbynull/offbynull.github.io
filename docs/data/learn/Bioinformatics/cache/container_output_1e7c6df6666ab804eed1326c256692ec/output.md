`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_FirstIndexesCheckpointed.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_FirstIndexesCheckpointed.py) (lines 100 to 116):`{bm-enable-all}`

```python
def walk_back_until_first_index_checkpoint(
        bwt_records: list[BWTRecord],
        bwt_first_indexes_checkpoints: dict[int, int],
        index: int
) -> int:
    walk_cnt = 0
    while index not in bwt_first_indexes_checkpoints:
        index = bwt_records[index].last_to_first_idx
        walk_cnt += 1
    first_idx = bwt_first_indexes_checkpoints[index] + walk_cnt
    # It's possible that the walk back continues backward before the start of the sequence, resulting
    # in it looping to the end and continuing to walk back from there. If that happens, the code below
    # adjusts it.
    sequence_len = len(bwt_records)
    if first_idx >= sequence_len:
        first_idx -= sequence_len
    return first_idx
```