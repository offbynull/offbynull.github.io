`{bm-disable-all}`[ch7_code/src/neighbour_detect/EdgeOnlyVariant.py](ch7_code/src/neighbour_detect/EdgeOnlyVariant.py) (lines 141 to 147):`{bm-enable-all}`

```python
def combine_count_and_normalize(g: Graph, leaf1: N, leaf2: N) -> Counter[E]:
    edge_counts = combined_count(g, leaf1, leaf2)
    leaf_count = get_leaf_count(g)
    path_edges = get_path(g, leaf1, leaf2)
    for e in path_edges:
        edge_counts[e] -= leaf_count - 2
    return edge_counts
```