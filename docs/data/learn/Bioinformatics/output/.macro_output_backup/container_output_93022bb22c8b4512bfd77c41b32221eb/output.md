`{bm-disable-all}`[ch7_code/src/phylogeny/UntrimTree.py](ch7_code/src/phylogeny/UntrimTree.py) (lines 110 to 148):`{bm-enable-all}`

```python
def untrim_tree(
        dist_mat: DistanceMatrix,
        trimmed_tree: Graph[N, ND, E, float],
        gen_node_id: Callable[[], N],
        gen_edge_id: Callable[[], E]
) -> None:
    # Which node was trimmed?
    n_trimmed = find_trimmed_leaf(dist_mat, trimmed_tree)
    # Find a pair whose path that goes through the trimmed node's parent
    n_start, n_end = find_pair_traveling_thru_leaf_parent(dist_mat, n_trimmed)
    # What's the distance from n_start to the trimmed node's parent?
    parent_dist = find_distance_to_leaf_parent(dist_mat, n_start, n_trimmed)
    # Walk the path from n_start to n_end, stopping once walk dist reaches parent_dist (where trimmed node's parent is)
    res = walk_until_distance(trimmed_tree, n_start, n_end, parent_dist)
    stopped_on = res[0]
    if stopped_on == 'NODE':
        # It stopped on an existing internal node -- the limb should be added to this node
        parent_n = res[1]
    elif stopped_on == 'EDGE':
        # It stopped on an edge -- a new internal node should be injected to break the edge, then the limb should extend
        # from that node.
        edge, n1, n2, walked_dist, edge_weight = res[1:]
        parent_n = gen_node_id()
        trimmed_tree.insert_node(parent_n)
        n1_to_parent_id = gen_edge_id()
        n1_to_parent_weight = parent_dist - walked_dist
        trimmed_tree.insert_edge(n1_to_parent_id, n1, parent_n, n1_to_parent_weight)
        parent_to_n2_id = gen_edge_id()
        parent_to_n2_weight = edge_weight - n1_to_parent_weight
        trimmed_tree.insert_edge(parent_to_n2_id, parent_n, n2, parent_to_n2_weight)
        trimmed_tree.delete_edge(edge)
    else:
        raise ValueError('???')
    # Add the limb
    limb_e = gen_edge_id()
    limb_len = find_limb_length(dist_mat, n_trimmed)
    trimmed_tree.insert_node(n_trimmed)
    trimmed_tree.insert_edge(limb_e, parent_n, n_trimmed, limb_len)
```