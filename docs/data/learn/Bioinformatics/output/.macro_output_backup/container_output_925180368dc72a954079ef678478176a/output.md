`{bm-disable-all}`[ch5_code/src/affine_gap_alignment/AffineGapAlignment_Basic_Graph.py](ch5_code/src/affine_gap_alignment/AffineGapAlignment_Basic_Graph.py) (lines 37 to 104):`{bm-enable-all}`

```python
def create_affine_gap_alignment_graph(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup,
        extended_gap_weight: float
) -> Graph[Tuple[int, ...], NodeData, str, EdgeData]:
    graph = create_grid_graph(
        [v, w],
        lambda n_id: NodeData(),
        lambda src_n_id, dst_n_id, offset, elems: EdgeData(elems[0], elems[1], weight_lookup.lookup(*elems))
    )
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    horizontal_indel_hop_edge_id_func = unique_id_generator('HORIZONTAL_INDEL_HOP')
    for from_c, r in product(range(v_node_count), range(w_node_count)):
        from_node_id = from_c, r
        for to_c in range(from_c + 2, v_node_count):
            to_node_id = to_c, r
            edge_id = horizontal_indel_hop_edge_id_func()
            v_elems = v[from_c:to_c]
            w_elems = [None] * len(v_elems)
            hop_count = to_c - from_c
            weight = weight_lookup.lookup(v_elems[0], w_elems[0]) + (hop_count - 1) * extended_gap_weight
            graph.insert_edge(edge_id, from_node_id, to_node_id, EdgeData(v_elems, w_elems, weight))
    vertical_indel_hop_edge_id_func = unique_id_generator('VERTICAL_INDEL_HOP')
    for c, from_r in product(range(v_node_count), range(w_node_count)):
        from_node_id = c, from_r
        for to_r in range(from_r + 2, w_node_count):
            to_node_id = c, to_r
            edge_id = vertical_indel_hop_edge_id_func()
            w_elems = w[from_r:to_r]
            v_elems = [None] * len(w_elems)
            hop_count = to_r - from_r
            weight = weight_lookup.lookup(v_elems[0], w_elems[0]) + (hop_count - 1) * extended_gap_weight
            graph.insert_edge(edge_id, from_node_id, to_node_id, EdgeData(v_elems, w_elems, weight))
    return graph


def affine_gap_alignment(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup,
        extended_gap_weight: float
) -> Tuple[float, List[str], List[Tuple[ELEM, ELEM]]]:
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    graph = create_affine_gap_alignment_graph(v, w, weight_lookup, extended_gap_weight)
    from_node = (0, 0)
    to_node = (v_node_count - 1, w_node_count - 1)
    populate_weights_and_backtrack_pointers(
        graph,
        from_node,
        lambda n_id, weight, e_id: graph.get_node_data(n_id).set_weight_and_backtracking_edge(weight, e_id),
        lambda n_id: graph.get_node_data(n_id).get_weight_and_backtracking_edge(),
        lambda e_id: graph.get_edge_data(e_id).weight
    )
    final_weight = graph.get_node_data(to_node).weight
    edges = backtrack(
        graph,
        to_node,
        lambda n_id: graph.get_node_data(n_id).get_weight_and_backtracking_edge()
    )
    alignment = []
    for e in edges:
        ed = graph.get_edge_data(e)
        alignment.append((ed.v_elem, ed.w_elem))
    return final_weight, edges, alignment
```