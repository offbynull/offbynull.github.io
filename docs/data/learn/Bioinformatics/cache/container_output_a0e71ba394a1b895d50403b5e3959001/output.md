`{bm-disable-all}`[ch7_code/src/phylogeny/FindLimbLength.py](ch7_code/src/phylogeny/FindLimbLength.py) (lines 22 to 28):`{bm-enable-all}`

```python
def find_limb_length(dm: DistanceMatrix[N], l: N) -> float:
    leaf_nodes = dm.leaf_ids()
    leaf_nodes.remove(l)
    a = leaf_nodes.pop()
    b = min(leaf_nodes, key=lambda x: (dm[l, a] + dm[l, x] - dm[a, x]) / 2)
    return (dm[l, a] + dm[l, b] - dm[a, b]) / 2
```