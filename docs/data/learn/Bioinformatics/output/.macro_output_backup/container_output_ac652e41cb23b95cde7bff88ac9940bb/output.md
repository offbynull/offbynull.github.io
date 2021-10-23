`{bm-disable-all}`[ch7_code/src/phylogeny/NeighbourJoiningMatrix.py](ch7_code/src/phylogeny/NeighbourJoiningMatrix.py) (lines 12 to 28):`{bm-enable-all}`

```python
def total_distance(dist_mat: DistanceMatrix[N]) -> dict[N, float]:
    ret = {}
    for l1 in dist_mat.leaf_ids():
        ret[l1] = sum(dist_mat[l1, l2] for l2 in dist_mat.leaf_ids())
    return ret


def neighbour_joining_matrix(dist_mat: DistanceMatrix[N]) -> DistanceMatrix[N]:
    tot_dists = total_distance(dist_mat)
    n = dist_mat.n
    ret = dist_mat.copy()
    for l1, l2 in product(dist_mat.leaf_ids(), repeat=2):
        if l1 == l2:
            continue
        ret[l1, l2] = tot_dists[l1] + tot_dists[l2] - (n - 2) * dist_mat[l1, l2]
    return ret
```