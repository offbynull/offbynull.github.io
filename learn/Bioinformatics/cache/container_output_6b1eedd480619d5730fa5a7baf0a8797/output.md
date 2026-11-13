`{bm-disable-all}`[ch5_code/src/global_alignment/GlobalAlignment_DivideAndConquer_NodeVariant.py](ch5_code/src/global_alignment/GlobalAlignment_DivideAndConquer_NodeVariant.py) (lines 11 to 40):`{bm-enable-all}`

```python
def find_max_alignment_path_nodes(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup,
        buffer: List[Tuple[int, int]],
        v_offset: int = 0,
        w_offset: int = 0) -> None:
    if len(v) == 0 or len(w) == 0:
        return
    c, r = find_node_that_max_alignment_path_travels_through_at_middle_col(v, w, weight_lookup)
    find_max_alignment_path_nodes(v[:c-1], w[:r-1], weight_lookup, buffer, v_offset=0, w_offset=0)
    buffer.append((v_offset + c, w_offset + r))
    find_max_alignment_path_nodes(v[c:], w[r:], weight_lookup, buffer, v_offset=v_offset+c, w_offset=v_offset+r)


def global_alignment(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup
) -> Tuple[float, List[Tuple[ELEM, ELEM]]]:
    nodes = [(0, 0)]
    find_max_alignment_path_nodes(v, w, weight_lookup, nodes)
    weight = 0.0
    alignment = []
    for (v_idx1, w_idx1), (v_idx2, w_idx2) in zip(nodes, nodes[1:]):
        sub_weight, sub_alignment = GlobalAlignment_Matrix.global_alignment(v[v_idx1:v_idx2], w[w_idx1:w_idx2], weight_lookup)
        weight += sub_weight
        alignment += sub_alignment
    return weight, alignment
```