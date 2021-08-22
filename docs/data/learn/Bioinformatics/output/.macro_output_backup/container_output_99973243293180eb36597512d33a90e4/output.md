`{bm-disable-all}`[ch7_code/src/neighbour_detect/EdgeOnlyVariant.py](ch7_code/src/neighbour_detect/EdgeOnlyVariant.py) (lines 68 to 72):`{bm-enable-all}`

```python
def combined_count(g: Graph, leaf1: N, leaf2: N) -> Counter[E]:
    leaf1_counts = count(g, leaf1)
    leaf2_counts = count(g, leaf2)
    return leaf1_counts + leaf2_counts
```