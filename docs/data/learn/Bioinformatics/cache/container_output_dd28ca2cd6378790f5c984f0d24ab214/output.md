`{bm-disable-all}`[ch8_code/src/clustering/KMeans_Lloyds.py](ch8_code/src/clustering/KMeans_Lloyds.py) (lines 148 to 172):`{bm-enable-all}`

```python
def k_means_lloyds(
        k: int,
        points: list[tuple[float]],
        centers_init: list[tuple[float]],
        dims: int,
        iteration_callback: IterationCallbackFunc
) -> MembershipAssignmentMap:
    old_centers = []
    centers = centers_init[:]
    while centers != old_centers:
        mapping = {c: [] for c in centers}
        # centers to clusters
        for pt in points:
            c, _ = find_closest_center(pt, centers)
            mapping[c].append(pt)
        # clusters to centers
        old_centers = centers
        centers = []
        for pts in mapping.values():
            new_c = center_of_gravity(pts, dims)
            centers.append(new_c)
        # notify of current iteration's cluster
        iteration_callback(mapping)
    return mapping
```