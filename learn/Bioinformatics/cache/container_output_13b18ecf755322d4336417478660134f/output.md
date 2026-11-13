`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_FirstIndexesCheckpointed.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_FirstIndexesCheckpointed.py) (lines 133 to 164):`{bm-enable-all}`

```python
def walk_find(
        bwt_records: list[BWTRecord],
        bwt_first_indexes_checkpoints: dict[int, int],
        test: str,
        start_row: int
) -> int | None:
    row = start_row
    for ch in reversed(test[:-1]):
        if bwt_records[row].last_ch != ch:
            return None
        row = bwt_records[row].last_to_first_ptr
    first_idx = walk_back_until_first_indexes_checkpoint(bwt_records, bwt_first_indexes_checkpoints, row)
    return first_idx


def find(
        bwt_records: list[BWTRecord],
        bwt_first_indexes_checkpoints: dict[int, int],
        test: str
) -> list[int]:
    found = []
    for i, rec in enumerate(bwt_records):
        if rec.first_ch == test[-1]:
            if len(test) == 1:
                first_idx = walk_back_until_first_indexes_checkpoint(bwt_records, bwt_first_indexes_checkpoints, i)
                found.append(first_idx)
            elif rec.last_ch == test[-2]:
                found_idx = walk_find(bwt_records, bwt_first_indexes_checkpoints, test, i)
                if found_idx is not None:
                    found.append(found_idx)
    return found
```