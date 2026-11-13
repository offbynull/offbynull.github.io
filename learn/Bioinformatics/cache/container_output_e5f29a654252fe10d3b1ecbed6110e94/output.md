`{bm-disable-all}`[ch5_code/src/fitting_alignment/FittingAlignment_Matrix.py](ch5_code/src/fitting_alignment/FittingAlignment_Matrix.py) (lines 10 to 93):`{bm-enable-all}`

```python
def backtrack(
        node_matrix: List[List[Any]]
) -> Tuple[float, List[Tuple[ELEM, ELEM]]]:
    v_node_idx = len(node_matrix) - 1
    w_node_idx = len(node_matrix[0]) - 1
    final_weight = node_matrix[v_node_idx][w_node_idx][0]
    alignment = []
    while v_node_idx != 0 or w_node_idx != 0:
        _, elems, backtrack_ptr = node_matrix[v_node_idx][w_node_idx]
        if backtrack_ptr == '↓':
            v_node_idx -= 1
            alignment.append(elems)
        elif backtrack_ptr == '→':
            w_node_idx -= 1
            alignment.append(elems)
        elif backtrack_ptr == '↘':
            v_node_idx -= 1
            w_node_idx -= 1
            alignment.append(elems)
        elif isinstance(backtrack_ptr, tuple):
            v_node_idx = backtrack_ptr[0]
            w_node_idx = backtrack_ptr[1]
    return final_weight, alignment[::-1]


def fitting_alignment(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup
) -> Tuple[float, List[Tuple[ELEM, ELEM]]]:
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    node_matrix = []
    for v_node_idx in range(v_node_count):
        row = []
        for w_node_idx in range(w_node_count):
            row.append([-1.0, (None, None), '?'])
        node_matrix.append(row)
    node_matrix[0][0][0] = 0.0           # source node weight
    node_matrix[0][0][1] = (None, None)  # source node elements (elements don't matter for source node)
    node_matrix[0][0][2] = '↘'           # source node backtracking edge (direction doesn't matter for source node)
    for v_node_idx, w_node_idx in product(range(v_node_count), range(w_node_count)):
        parents = []
        if v_node_idx > 0 and w_node_idx > 0:
            v_elem = v[v_node_idx - 1]
            w_elem = w[w_node_idx - 1]
            parents.append([
                node_matrix[v_node_idx - 1][w_node_idx - 1][0] + weight_lookup.lookup(v_elem, w_elem),
                (v_elem, w_elem),
                '↘'
            ])
        if v_node_idx > 0:
            v_elem = v[v_node_idx - 1]
            parents.append([
                node_matrix[v_node_idx - 1][w_node_idx][0] + weight_lookup.lookup(v_elem, None),
                (v_elem, None),
                '↓'
            ])
        if w_node_idx > 0:
            w_elem = w[w_node_idx - 1]
            parents.append([
                node_matrix[v_node_idx][w_node_idx - 1][0] + weight_lookup.lookup(None, w_elem),
                (None, w_elem),
                '→'
            ])
        # If first column but not source node, consider free-ride from source node
        if v_node_idx == 0 and w_node_idx != 0:
            parents.append([
                0.0,
                (None, None),
                (0, 0)  # jump to source
            ])
        # If sink node, consider free-rides coming from every node in last column that isn't sink node
        if v_node_idx == v_node_count - 1 and w_node_idx == w_node_count - 1:
            for w_node_idx_from in range(w_node_count - 1):
                parents.append([
                    node_matrix[v_node_idx][w_node_idx_from][0] + 0.0,
                    (None, None),
                    (v_node_idx, w_node_idx_from)  # jump to this position
                ])
        if parents:  # parents will be empty if v_node_idx and w_node_idx were both 0
            node_matrix[v_node_idx][w_node_idx] = max(parents, key=lambda x: x[0])
    return backtrack(node_matrix)
```