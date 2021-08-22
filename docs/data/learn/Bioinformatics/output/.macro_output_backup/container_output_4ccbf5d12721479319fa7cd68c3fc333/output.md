`{bm-disable-all}`[ch7_code/src/neighbour_detect/EdgeOnlyVariant.py](ch7_code/src/neighbour_detect/EdgeOnlyVariant.py) (lines 85 to 99):`{bm-enable-all}`

```python
def count(g: Graph, leaf_id: N) -> Counter[E]:
    # Collect paths from leaf_id to all other leaf nodes
    path_collection = []
    for other_leaf_id in get_leaf_nodes(g):
        if leaf_id == other_leaf_id:
            continue
        path = get_path(g, leaf_id, other_leaf_id)
        path_collection.append(path)
    # Count edges across all paths
    edge_counts = Counter()
    for path in path_collection:
        edge_counts.update(path)
    # Return edge counts
    return edge_counts
```