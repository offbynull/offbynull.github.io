`{bm-disable-all}`[ch7_code/src/neighbour_detect/EdgeOnlyVariant.py](ch7_code/src/neighbour_detect/EdgeOnlyVariant.py) (lines 118 to 121):`{bm-enable-all}`

```python
def combined_count(g: Graph, leaf1: N, leaf2: N) -> Counter[E]:
    c1 = count(g, leaf1)
    c2 = count(g, leaf2)
    return c1 + c2
```