`{bm-disable-all}`[ch7_code/src/neighbour_detect/EdgeOnlyVariant.py](ch7_code/src/neighbour_detect/EdgeOnlyVariant.py) (lines 56 to 64):`{bm-enable-all}`

```python
def count(g: Graph, leaf: N) -> Counter[E]:
    counter = Counter()
    leaf_list = get_leaf_nodes(g)
    leaf_list.remove(leaf)
    for other_leaf in leaf_list:
        edges = path(g, leaf, other_leaf)
        counter.update(edges)
    return counter
```