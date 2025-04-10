`{bm-disable-all}`[ch5_code/src/global_alignment/Global_FindEdgeThatMaxAlignmentPathTravelsThroughAtColumn.py](ch5_code/src/global_alignment/Global_FindEdgeThatMaxAlignmentPathTravelsThroughAtColumn.py) (lines 10 to 65):`{bm-enable-all}`

```python
def find_edge_that_max_alignment_path_travels_through_at_col(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup,
        col: int
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    sc = SweepCombiner(v, w, weight_lookup)
    # Get max node in column -- max alignment path guaranteed to go through here.
    col_vals = sc.get_col(col)
    row, _ = max(enumerate(col_vals), key=lambda x: x[1])
    # Check node immediately to the right, down, right-down (diag) -- the ones with the max value MAY form the edge that
    # the max alignment path goes through. Recall that the max value will be the same max value as the one from col_vals
    # (weight of the final alignment path / sink node in the full alignment graph).
    #
    # Of the ones WITH the max value, check the weights formed by each edge. The one with the highest edge weight is the
    # edge that the max alignment path goes through (if there's more than 1, it means there's more than 1 max alignment
    # path -- one is picked at random).
    neighbours = []
    next_col_vals = sc.get_col(col + 1) if col + 1 < v_node_count else None  # very quick due to prev call to get_col()
    if col + 1 < v_node_count:
        right_weight = next_col_vals[row]
        right_node = (col + 1, row)
        v_elem = v[col - 1]
        w_elem = None
        edge_weight = weight_lookup.lookup(v_elem, w_elem)
        neighbours += [(right_weight, edge_weight, right_node)]
    if row + 1 < w_node_count:
        down_weight = col_vals[row + 1]
        down_node = (col, row + 1)
        v_elem = None
        w_elem = w[row - 1]
        edge_weight = weight_lookup.lookup(v_elem, w_elem)
        neighbours += [(down_weight, edge_weight, down_node)]
    if col + 1 < v_node_count and row + 1 < w_node_count:
        downright_weight = next_col_vals[row + 1]
        downright_node = (col + 1, row + 1)
        v_elem = v[col - 1]
        w_elem = w[row - 1]
        edge_weight = weight_lookup.lookup(v_elem, w_elem)
        neighbours += [(downright_weight, edge_weight, downright_node)]
    neighbours.sort(key=lambda x: x[:2])  # sort by weight, then edge weight
    _, _, (col2, row2) = neighbours[-1]
    return (col, row), (col2, row2)


def find_edge_that_max_alignment_path_travels_through_at_middle_col(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    v_node_count = len(v) + 1
    middle_col_idx = (v_node_count - 1) // 2
    return find_edge_that_max_alignment_path_travels_through_at_col(v, w, weight_lookup, middle_col_idx)
```