`{bm-disable-all}`[ch8_code/src/clustering/KMeans_Lloyds.py](ch8_code/src/clustering/KMeans_Lloyds.py) (lines 138 to 169):`{bm-enable-all}`

```python
def k_means_lloyds(
        k: int,
        vectors: list[Sequence[float]],
        centers_init: list[Sequence[float]],
        dims: int,
        iteration_callback: Callable[  # callback func to invoke on each iteration
            [
                dict[tuple[float], list[Sequence[float]]]
            ],
            None
        ] | None = None
) -> dict[tuple[float], list[Sequence[float]]]:
    old_centers = []
    centers = centers_init[:]
    while centers != old_centers:
        mapping = {tuple(ct_pt): [] for ct_pt in centers}
        # centers to clusters
        for pt in vectors:
            ct_pt, _ = find_closest_center(pt, centers)
            ct_pt = tuple(ct_pt)
            mapping[ct_pt].append(pt)
        # clusters to centers
        old_centers = centers
        centers = []
        for pts in mapping.values():
            new_ct_pt = center_of_gravity(pts, dims)
            new_ct_pt = tuple(new_ct_pt)
            centers.append(new_ct_pt)
        # notify of current iteration's cluster
        iteration_callback(mapping)
    return mapping
```