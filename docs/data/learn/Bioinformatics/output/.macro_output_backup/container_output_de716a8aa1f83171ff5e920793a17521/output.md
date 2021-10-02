`{bm-disable-all}`[ch7_code/src/phylogeny/UntrimTree.py](ch7_code/src/phylogeny/UntrimTree.py) (lines 65 to 77):`{bm-enable-all}`

```python
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
```