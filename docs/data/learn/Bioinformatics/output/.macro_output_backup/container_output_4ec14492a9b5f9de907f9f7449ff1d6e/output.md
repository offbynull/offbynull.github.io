```python
def reduced_to_2_check(self, l1: N, l2: N) -> bool:
    p = self.path(l1, l2)
    c = self.combine_edge_count_and_normalize(l1, l2)
    return all(c[edge] == 2 for edge in p)  # if counts for all edges in p reduced to 2
```