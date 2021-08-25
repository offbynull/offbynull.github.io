```python
def combine_edge_multiple(self, l1: N, l2: N) -> Counter[E]:
    c1 = self.edge_multiple(l1)
    c2 = self.edge_multiple(l2)
    return c1 + c2
```