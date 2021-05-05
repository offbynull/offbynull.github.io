`{bm-disable-all}`[ch5_code/src/overlap_alignment/OverlapAlignment_Graph.py](ch5_code/src/overlap_alignment/OverlapAlignment_Graph.py) (lines 37 to 95):`{bm-enable-all}`

```python
def create_overlap_alignment_graph(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup
) -> Graph[Tuple[int, ...], NodeData, str, EdgeData]:
    graph = create_grid_graph(
        [v, w],
        lambda n_id: NodeData(),
        lambda src_n_id, dst_n_id, offset, elems: EdgeData(elems[0], elems[1], weight_lookup.lookup(*elems))
    )
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    source_node = 0, 0
    source_create_free_ride_edge_id_func = unique_id_generator('FREE_RIDE_SOURCE')
    for node in product([0], range(w_node_count)):
        if node == source_node:
            continue
        e = source_create_free_ride_edge_id_func()
        graph.insert_edge(e, source_node, node, EdgeData(None, None, 0.0))
    sink_node = v_node_count - 1, w_node_count - 1
    sink_create_free_ride_edge_id_func = unique_id_generator('FREE_RIDE_SINK')
    for node in product(range(v_node_count), [w_node_count - 1]):
        if node == sink_node:
            continue
        e = sink_create_free_ride_edge_id_func()
        graph.insert_edge(e, node, sink_node, EdgeData(None, None, 0.0))
    return graph


def overlap_alignment(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup
) -> Tuple[float, List[str], List[Tuple[ELEM, ELEM]]]:
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    graph = create_overlap_alignment_graph(v, w, weight_lookup)
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
    alignment_edges = list(filter(lambda e: not e.startswith('FREE_RIDE'), edges))  # remove free rides from list
    alignment = []
    for e in alignment_edges:
        ed = graph.get_edge_data(e)
        alignment.append((ed.v_elem, ed.w_elem))
    return final_weight, edges, alignment
```