`{bm-disable-all}`[ch7_code/src/phylogeny/UntrimTree.py](ch7_code/src/phylogeny/UntrimTree.py) (lines 54 to 136):`{bm-enable-all}`

```python
def find_trimmed_leaf(dist_mat: DistanceMatrix[N], trimmed_tree: Graph[N, ND, E, float]) -> N:
    trimmed_tree_leaves = {n for n in trimmed_tree.get_nodes() if trimmed_tree.get_degree(n) == 1}
    dist_mat_leaves = dist_mat.leaf_ids()
    if len(dist_mat_leaves) - 1 != len(trimmed_tree_leaves):
        raise ValueError(f'Bad inputs {dist_mat_leaves} vs {trimmed_tree_leaves}')
    leaves_diff = dist_mat_leaves - trimmed_tree_leaves
    if len(leaves_diff) != 1:
        raise ValueError(f'Bad inputs {leaves_diff}')
    return leaves_diff.pop()


def find_pair_traveling_thru_leaf_parent(dist_mat: DistanceMatrix, leaf_node: N) -> tuple[N, N]:
    leaf_set = dist_mat.leaf_ids() - {leaf_node}
    for l1, l2 in product(leaf_set, repeat=2):
        if not is_same_subtree(dist_mat, leaf_node, l1, l2):
            return l1, l2
    raise ValueError('Not found')


def find_distance_to_leaf_parent(dist_mat: DistanceMatrix, from_leaf_node: N, to_leaf_node: N) -> float:
    balded_dist_mat = dist_mat.copy()
    bald_distance_matrix(balded_dist_mat, to_leaf_node)
    return balded_dist_mat[from_leaf_node, to_leaf_node]


def walk_until_distance(
        tree: Graph[N, ND, E, float],
        n_start: N,
        n_end: N,
        desired_dist: float
) -> Union[
    tuple[Literal['NODE'], N],
    tuple[Literal['EDGE'], E, N, N, float, float]
]:
    path = find_path(tree, n_start, n_end)
    last_edge_end = n_start
    dist_walked = 0.0
    for edge in path:
        ends = tree.get_edge_ends(edge)
        n1 = last_edge_end
        n2 = next(n for n in ends if n != last_edge_end)
        weight = tree.get_edge_data(edge)
        dist_walked_with_weight = dist_walked + weight
        if dist_walked_with_weight > desired_dist:
            return 'EDGE', edge, n1, n2, dist_walked, weight
        elif dist_walked_with_weight == desired_dist:
            return 'NODE', n2
        dist_walked = dist_walked_with_weight
        last_edge_end = n2
    raise ValueError('Bad inputs')


def untrim_tree(
        dist_mat: DistanceMatrix,
        trimmed_tree: Graph[N, ND, E, float],
        node_id_generator: Callable[[], N],
        edge_id_generator: Callable[[], E]
) -> None:
    trimmed_n = find_trimmed_leaf(dist_mat, trimmed_tree)
    trimmed_limb_len = find_limb_length(dist_mat, trimmed_n)
    leaf1, leaf2 = find_pair_traveling_thru_leaf_parent(dist_mat, trimmed_n)
    trimmed_parent_dist = find_distance_to_leaf_parent(dist_mat, leaf1, trimmed_n)
    res = walk_until_distance(trimmed_tree, leaf1, leaf2, trimmed_parent_dist)
    stopped_on = res[0]
    if stopped_on == 'NODE':
        parent_n = res[1]
    elif stopped_on == 'EDGE':
        edge, n1, n2, walked_dist, edge_weight = res[1:]
        parent_n = node_id_generator()
        trimmed_tree.insert_node(parent_n)
        n1_to_parent_id = edge_id_generator()
        n1_to_parent_weight = trimmed_parent_dist - walked_dist
        trimmed_tree.insert_edge(n1_to_parent_id, n1, parent_n, n1_to_parent_weight)
        parent_to_n2_id = edge_id_generator()
        parent_to_n2_weight = edge_weight - n1_to_parent_weight
        trimmed_tree.insert_edge(parent_to_n2_id, parent_n, n2, parent_to_n2_weight)
        trimmed_tree.delete_edge(edge)
    else:
        raise ValueError('???')
    limb_e = edge_id_generator()
    trimmed_tree.insert_node(trimmed_n)
    trimmed_tree.insert_edge(limb_e, parent_n, trimmed_n, trimmed_limb_len)
```