```python
def combine_edge_multiple_and_normalize(self, l1: N, l2: N) -> Counter[E]:
    edge_multiples = self.combine_edge_multiple(l1, l2)
    path_edges = self.path(l1, l2)
    for e in path_edges:
        edge_multiples[e] -= (self.leaf_count - 2) * self.tree.get_edge_data(e)
    return edge_multiples
```