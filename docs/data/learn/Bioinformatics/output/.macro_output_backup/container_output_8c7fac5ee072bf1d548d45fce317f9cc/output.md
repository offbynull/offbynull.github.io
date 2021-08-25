`{bm-disable-all}`[ch5_code/src/global_alignment/GlobalAlignment_DivideAndConquer_EdgeVariant.py](ch5_code/src/global_alignment/GlobalAlignment_DivideAndConquer_EdgeVariant.py) (lines 10 to 80):`{bm-enable-all}`

```python
def find_max_alignment_path_edges(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup,
        top: int,
        bottom: int,
        left: int,
        right: int,
        output: List[str]):
    if left == right:
        for i in range(top, bottom):
            output += ['↓']
        return
    if top == bottom:
        for i in range(left, right):
            output += ['→']
        return

    (col1, row1), (col2, row2) = find_edge_that_max_alignment_path_travels_through_at_middle_col(v[left:right], w[top:bottom], weight_lookup)
    middle_col = left + col1
    middle_row = top + row1
    find_max_alignment_path_edges(v, w, weight_lookup, top, middle_row, left, middle_col, output)
    if row1 + 1 == row2 and col1 + 1 == col2:
        edge_dir = '↘'
    elif row1 == row2 and col1 + 1 == col2:
        edge_dir = '→'
    elif row1 + 1 == row2 and col1 == col2:
        edge_dir = '↓'
    else:
        raise ValueError()
    if edge_dir == '→' or edge_dir == '↘':
        middle_col += 1
    if edge_dir == '↓' or edge_dir == '↘':
        middle_row += 1
    output += [edge_dir]
    find_max_alignment_path_edges(v, w, weight_lookup, middle_row, bottom, middle_col, right, output)


def global_alignment(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup
) -> Tuple[float, List[Tuple[ELEM, ELEM]]]:
    edges = []
    find_max_alignment_path_edges(v, w, weight_lookup, 0, len(w), 0, len(v), edges)
    weight = 0.0
    alignment = []
    v_idx = 0
    w_idx = 0
    for edge in edges:
        if edge == '→':
            v_elem = v[v_idx]
            w_elem = None
            alignment.append((v_elem, w_elem))
            weight += weight_lookup.lookup(v_elem, w_elem)
            v_idx += 1
        elif edge == '↓':
            v_elem = None
            w_elem = w[w_idx]
            alignment.append((v_elem, w_elem))
            weight += weight_lookup.lookup(v_elem, w_elem)
            w_idx += 1
        elif edge == '↘':
            v_elem = v[v_idx]
            w_elem = w[w_idx]
            alignment.append((v_elem, w_elem))
            weight += weight_lookup.lookup(v_elem, w_elem)
            v_idx += 1
            w_idx += 1
    return weight, alignment
```