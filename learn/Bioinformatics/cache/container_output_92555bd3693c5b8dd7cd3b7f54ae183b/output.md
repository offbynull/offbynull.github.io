```python
def neighbour_check(self, l1: N, l2: N) -> bool:
    path_edges = self.path(l1, l2)
    return len(path_edges) == 2
```