`{bm-disable-all}`[ch7_code/src/neighbour_detect/EdgeCountExplainer.py](ch7_code/src/neighbour_detect/EdgeCountExplainer.py) (lines 127 to 137):`{bm-enable-all}`

```python
def neighbour_detect(self) -> tuple[int, tuple[N, N]]:
    found_pair = None
    found_total_count = -1
    for l1, l2 in combinations(self.leaf_nodes, r=2):
        normalized_counts = self.combine_edge_count_and_normalize(l1, l2)
        total_count = sum(c for c in normalized_counts.values())
        if total_count > found_total_count:
            found_pair = l1, l2
            found_total_count = total_count
    return found_total_count, found_pair
```