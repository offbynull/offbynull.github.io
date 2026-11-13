```python
def edge_count(self, l1: N) -> Counter[E]:
    # Collect paths from l1 to all other leaf nodes
    path_collection = []
    for l2 in self.leaf_nodes:
        if l1 == l2:
            continue
        path = self.path(l1, l2)
        path_collection.append(path)
    # Count edges across all paths
    edge_counts = Counter()
    for path in path_collection:
        edge_counts.update(path)
    # Return edge counts
    return edge_counts
```