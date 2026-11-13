`{bm-disable-all}`[ch8_code/src/clustering/Soft_HierarchialClustering_NeighbourJoining_v2.py](ch8_code/src/clustering/Soft_HierarchialClustering_NeighbourJoining_v2.py) (lines 102 to 117):`{bm-enable-all}`

```python
def merge_overlaps(
        n_leaf: str,
        internal_to_leaves: dict[str, str],
        leaves_to_internal: dict[str, str]
):
    prev_n_leaves_len = 0
    prev_n_internals_len = 0
    n_leaves = {n_leaf}
    n_internals = {}
    while prev_n_internals_len != len(n_internals) or prev_n_leaves_len != len(n_leaves):
        prev_n_internals_len = len(n_internals)
        prev_n_leaves_len = len(n_leaves)
        n_internals = {n_i for n_l in n_leaves for n_i in leaves_to_internal[n_l]}
        n_leaves = {n_l for n_i in n_internals for n_l in internal_to_leaves[n_i]}
    return n_leaves, n_internals
```