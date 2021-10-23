`{bm-disable-all}`[ch7_code/src/phylogeny/Balder.py](ch7_code/src/phylogeny/Balder.py) (lines 16 to 29):`{bm-enable-all}`

```python
def bald_distance_matrix(dm: DistanceMatrix, leaf: N) -> None:
    limb_len = find_limb_length(dm, leaf)
    for n in dm.leaf_ids_it():
        if n == leaf:
            continue
        dm[leaf, n] -= limb_len


def bald_tree(tree: Graph[N, ND, E, float], leaf: N) -> None:
    if tree.get_degree(leaf) != 1:
        raise ValueError('Not a leaf node')
    limb = next(tree.get_outputs(leaf))
    tree.update_edge_data(limb, 0.0)
```