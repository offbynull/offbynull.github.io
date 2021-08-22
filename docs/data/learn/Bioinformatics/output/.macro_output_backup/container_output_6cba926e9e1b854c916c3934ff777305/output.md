`{bm-disable-all}`[ch7_code/src/neighbour_detect/EdgeOnlyVariant.py](ch7_code/src/neighbour_detect/EdgeOnlyVariant.py) (lines 76 to 82):`{bm-enable-all}`

```python
def normalized_combined_count(g: Graph, leaf1: N, leaf2: N) -> Counter[E]:
    leaf_count = get_leaf_count(g)
    edge_counts = combined_count(g, leaf1, leaf2)
    path_edges = path(g, leaf1, leaf2)
    for edge in path_edges:
        edge_counts[edge] -= leaf_count - 2
    return edge_counts
```