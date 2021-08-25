`{bm-disable-all}`[ch5_code/src/global_alignment/GlobalMultipleAlignment_Graph.py](ch5_code/src/global_alignment/GlobalMultipleAlignment_Graph.py) (lines 33 to 71):`{bm-enable-all}`

```python
def create_global_alignment_graph(
        seqs: List[List[ELEM]],
        weight_lookup: WeightLookup
) -> Graph[Tuple[int, ...], NodeData, str, EdgeData]:
    graph = create_grid_graph(
        seqs,
        lambda n_id: NodeData(),
        lambda src_n_id, dst_n_id, offset, elems: EdgeData(elems, weight_lookup.lookup(*elems))
    )
    return graph


def global_alignment(
        seqs: List[List[ELEM]],
        weight_lookup: WeightLookup
) -> Tuple[float, List[str], List[Tuple[ELEM, ...]]]:
    seq_node_counts = [len(s) for s in seqs]
    graph = create_global_alignment_graph(seqs, weight_lookup)
    from_node = tuple([0] * len(seqs))
    to_node = tuple(seq_node_counts)
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
        alignment.append(ed.elems)
    return final_weight, edges, alignment
```