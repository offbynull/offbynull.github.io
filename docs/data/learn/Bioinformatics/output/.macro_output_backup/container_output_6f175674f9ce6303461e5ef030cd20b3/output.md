`{bm-disable-all}`[ch5_code/src/affine_gap_alignment/AffineGapAlignment_Layer_Graph.py](ch5_code/src/affine_gap_alignment/AffineGapAlignment_Layer_Graph.py) (lines 37 to 135):`{bm-enable-all}`

```python
def create_affine_gap_alignment_graph(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup,
        extended_gap_weight: float
) -> Graph[Tuple[int, ...], NodeData, str, EdgeData]:
    graph_low = create_grid_graph(
        [v, w],
        lambda n_id: NodeData(),
        lambda src_n_id, dst_n_id, offset, elems: EdgeData(elems[0], elems[1], extended_gap_weight) if offset == (1, 0) else None
    )
    graph_mid = create_grid_graph(
        [v, w],
        lambda n_id: NodeData(),
        lambda src_n_id, dst_n_id, offset, elems: EdgeData(elems[0], elems[1], weight_lookup.lookup(*elems)) if offset == (1, 1) else None
    )
    graph_high = create_grid_graph(
        [v, w],
        lambda n_id: NodeData(),
        lambda src_n_id, dst_n_id, offset, elems: EdgeData(elems[0], elems[1], extended_gap_weight) if offset == (0, 1) else None
    )

    graph_merged = Graph()
    create_edge_id_func = unique_id_generator('E')

    def merge(from_graph, n_prefix):
        for n_id in from_graph.get_nodes():
            n_data = from_graph.get_node_data(n_id)
            graph_merged.insert_node(n_prefix + n_id, n_data)
        for e_id in from_graph.get_edges():
            from_n_id, to_n_id, e_data = from_graph.get_edge(e_id)
            graph_merged.insert_edge(create_edge_id_func(), n_prefix + from_n_id, n_prefix + to_n_id, e_data)

    merge(graph_low, ('high', ))
    merge(graph_mid, ('mid',))
    merge(graph_high, ('low',))

    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    mid_to_low_edge_id_func = unique_id_generator('MID_TO_LOW')
    for r, c in product(range(v_node_count - 1), range(w_node_count)):
        from_n_id = 'mid', r, c
        to_n_id = 'high', r + 1, c
        e = mid_to_low_edge_id_func()
        graph_merged.insert_edge(e, from_n_id, to_n_id, EdgeData(v[r], None, weight_lookup.lookup(v[r], None)))
    low_to_mid_edge_id_func = unique_id_generator('HIGH_TO_MID')
    for r, c in product(range(1, v_node_count), range(w_node_count)):
        from_n_id = 'high', r, c
        to_n_id = 'mid', r, c
        e = low_to_mid_edge_id_func()
        graph_merged.insert_edge(e, from_n_id, to_n_id, EdgeData(None, None, 0.0))
    mid_to_high_edge_id_func = unique_id_generator('MID_TO_HIGH')
    for r, c in product(range(v_node_count), range(w_node_count - 1)):
        from_n_id = 'mid', r, c
        to_n_id = 'low', r, c + 1
        e = mid_to_high_edge_id_func()
        graph_merged.insert_edge(e, from_n_id, to_n_id, EdgeData(None, w[c], weight_lookup.lookup(None, w[c])))
    high_to_mid_edge_id_func = unique_id_generator('LOW_TO_MID')
    for r, c in product(range(v_node_count), range(1, w_node_count)):
        from_n_id = 'low', r, c
        to_n_id = 'mid', r, c
        e = high_to_mid_edge_id_func()
        graph_merged.insert_edge(e, from_n_id, to_n_id, EdgeData(None, None, 0.0))

    return graph_merged


def affine_gap_alignment(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup,
        extended_gap_weight: float
) -> Tuple[float, List[str], List[Tuple[ELEM, ELEM]]]:
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    graph = create_affine_gap_alignment_graph(v, w, weight_lookup, extended_gap_weight)
    from_node = ('mid', 0, 0)
    to_node = ('mid', v_node_count - 1, w_node_count - 1)
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
    edges = list(filter(lambda e: not e.startswith('LOW_TO_MID'), edges))  # remove free rides from list
    edges = list(filter(lambda e: not e.startswith('HIGH_TO_MID'), edges))  # remove free rides from list
    alignment = []
    for e in edges:
        ed = graph.get_edge_data(e)
        alignment.append((ed.v_elem, ed.w_elem))
    return final_weight, edges, alignment
```