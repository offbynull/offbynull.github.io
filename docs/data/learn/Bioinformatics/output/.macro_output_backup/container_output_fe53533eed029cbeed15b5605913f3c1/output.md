`{bm-disable-all}`[ch7_code/src/phylogeny/ApproximateLimbLength.py](ch7_code/src/phylogeny/ApproximateLimbLength.py) (lines 14 to 23):`{bm-enable-all}`

```python
def approximate_limb_length(dm: DistanceMatrix, l: N, l_neighbour: N):
    leaf_nodes = dm.leaf_ids()
    leaf_nodes.remove(l)
    leaf_nodes.remove(l_neighbour)
    lengths = []
    for k in leaf_nodes:
        length = (dm[l, l_neighbour] + dm[l, k] - dm[l_neighbour, k]) / 2
        lengths.append(length)
    return mean(lengths)
```