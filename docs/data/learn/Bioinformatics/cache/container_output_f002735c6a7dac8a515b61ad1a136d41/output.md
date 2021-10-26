`{bm-disable-all}`[ch5_code/src/global_alignment/Global_FindNodeThatMaxAlignmentPathTravelsThroughAtColumn.py](ch5_code/src/global_alignment/Global_FindNodeThatMaxAlignmentPathTravelsThroughAtColumn.py) (lines 10 to 29):`{bm-enable-all}`

```python
def find_node_that_max_alignment_path_travels_through_at_col(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup,
        col: int
) -> Tuple[int, int]:
    col_vals = SweepCombiner(v, w, weight_lookup).get_col(col)
    row, _ = max(enumerate(col_vals), key=lambda x: x[1])
    return col, row


def find_node_that_max_alignment_path_travels_through_at_middle_col(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup
) -> Tuple[int, int]:
    v_node_count = len(v) + 1
    middle_col_idx = v_node_count // 2
    return find_node_that_max_alignment_path_travels_through_at_col(v, w, weight_lookup, middle_col_idx)
```