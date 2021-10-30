`{bm-disable-all}`[ch7_code/src/phylogeny/NeighbourJoiningMatrix.py](ch7_code/src/phylogeny/NeighbourJoiningMatrix.py) (lines 21 to 49):`{bm-enable-all}`

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


def find_neighbours(dist_mat: DistanceMatrix[N]) -> tuple[N, N]:
    nj_mat = neighbour_joining_matrix(dist_mat)
    found_pair = None
    found_nj_val = -1
    for l1, l2 in product(nj_mat.leaf_ids_it(), repeat=2):
        if nj_mat[l1, l2] > found_nj_val:
            found_pair = l1, l2
            found_nj_val = nj_mat[l1, l2]
    assert found_pair is not None
    return found_pair
```