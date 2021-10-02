`{bm-disable-all}`[ch7_code/src/phylogeny/Trimmer.py](ch7_code/src/phylogeny/Trimmer.py) (lines 17 to 28):`{bm-enable-all}`

```python
def trim_distance_matrix(dm: DistanceMatrix, leaf: N) -> None:
    dm.delete(leaf)  # remove row+col for leaf


def trim_tree(tree: Graph[N, ND, E, float], leaf: N) -> None:
    if tree.get_degree(leaf) != 1:
        raise ValueError('Not a leaf node')
    edge = next(tree.get_outputs(leaf))
    tree.delete_edge(edge)
    tree.delete_node(leaf)
    merge_nodes_of_degree2(tree)
```