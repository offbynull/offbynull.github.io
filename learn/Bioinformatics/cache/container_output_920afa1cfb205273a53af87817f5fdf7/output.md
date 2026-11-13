`{bm-disable-all}`[ch5_code/src/graph/GraphGridCreate.py](ch5_code/src/graph/GraphGridCreate.py) (lines 31 to 58):`{bm-enable-all}`

```python
def create_grid_graph(
        sequences: List[List[ELEM]],
        on_new_node: ON_NEW_NODE_FUNC_TYPE,
        on_new_edge: ON_NEW_EDGE_FUNC_TYPE
) -> Graph[Tuple[int, ...], ND, str, ED]:
    create_edge_id_func = unique_id_generator('E')
    graph = Graph()
    axes = [[None] + av for av in sequences]
    axes_len = [range(len(axis)) for axis in axes]
    for grid_coord in product(*axes_len):
        node_data = on_new_node(grid_coord)
        if node_data is not None:
            graph.insert_node(grid_coord, node_data)
    for src_grid_coord in graph.get_nodes():
        for grid_coord_offsets in product([0, 1], repeat=len(sequences)):
            dst_grid_coord = tuple(axis + offset for axis, offset in zip(src_grid_coord, grid_coord_offsets))
            if src_grid_coord == dst_grid_coord:  # skip if making a connection to self
                continue
            if not graph.has_node(dst_grid_coord):  # skip if neighbouring node doesn't exist
                continue
            elements = tuple(None if src_idx == dst_idx else axes[axis_idx][dst_idx]
                             for axis_idx, (src_idx, dst_idx) in enumerate(zip(src_grid_coord, dst_grid_coord)))
            edge_data = on_new_edge(src_grid_coord, dst_grid_coord, grid_coord_offsets, elements)
            if edge_data is not None:
                edge_id = create_edge_id_func()
                graph.insert_edge(edge_id, src_grid_coord, dst_grid_coord, edge_data)
    return graph
```