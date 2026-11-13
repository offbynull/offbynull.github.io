`{bm-disable-all}`[ch7_code/src/phylogeny/FindNeighbourLimbLengths_Optimized.py](ch7_code/src/phylogeny/FindNeighbourLimbLengths_Optimized.py) (lines 21 to 28):`{bm-enable-all}`

```python
def find_neighbouring_limb_lengths(dm: DistanceMatrix[N], l1: N, l2: N) -> tuple[float, float]:
    l1_dist_sum = sum(dm[l1, k] for k in dm.leaf_ids())
    l2_dist_sum = sum(dm[l2, k] for k in dm.leaf_ids())
    res = (l1_dist_sum - l2_dist_sum) / (dm.n - 2)
    l1_len = (dm[l1, l2] + res) / 2
    l2_len = (dm[l1, l2] - res) / 2
    return l1_len, l2_len
```