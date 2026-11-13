`{bm-disable-all}`[ch7_code/src/phylogeny/UPGMA.py](ch7_code/src/phylogeny/UPGMA.py) (lines 64 to 70):`{bm-enable-all}`

```python
def cluster_dist(dm_orig: DistanceMatrix[N], c_set: ClusterSet, c1: str, c2: str) -> float:
    c1_set = c_set[c1]  # this should be a set of leaf nodes from the ORIGINAL unmodified distance matrix
    c2_set = c_set[c2]  # this should be a set of leaf nodes from the ORIGINAL unmodified distance matrix
    numerator = sum(dm_orig[i, j] for i, j in product(c1_set, c2_set))  # sum it all up
    denominator = len(c1_set) * len(c2_set)  # number of additions that occurred
    return numerator / denominator
```