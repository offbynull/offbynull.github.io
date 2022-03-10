`{bm-disable-all}`[ch8_code/src/clustering/Soft_HierarchialClustering_NeighbourJoining_v2.py](ch8_code/src/clustering/Soft_HierarchialClustering_NeighbourJoining_v2.py) (lines 124 to 134):`{bm-enable-all}`

```python
def mean_dist_within_edge_range(
        tree: Graph[str, None, str, float],
        range: tuple[float, float] = (0.4, 0.6)
) -> float:
    dists = [tree.get_edge_data(e) for e in tree.get_edges()]
    dists.sort()
    dists_start_idx = int(range[0] * len(dists))
    dists_end_idx = int(range[1] * len(dists) + 1)
    dist_capture = mean(dists[dists_start_idx:dists_end_idx])
    return dist_capture
```