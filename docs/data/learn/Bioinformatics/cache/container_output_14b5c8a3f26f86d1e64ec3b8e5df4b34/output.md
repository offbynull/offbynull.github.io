```python
def combine_edge_count(self, l1: N, l2: N) -> Counter[E]:
    c1 = self.edge_count(l1)
    c2 = self.edge_count(l2)
    return c1 + c2
```