`{bm-disable-all}`[ch8_code/src/clustering/KCenters_FarthestFirstTraversal.py](ch8_code/src/clustering/KCenters_FarthestFirstTraversal.py) (lines 118 to 168):`{bm-enable-all}`

```python
def find_closest_center(data_pt, center_pts):
    center_pt = min(
        center_pts,
        key=lambda cp: dist(data_pt, cp)
    )
    return center_pt, dist(center_pt, data_pt)


def centers_to_clusters(
        centers: list[tuple[float]],
        vectors: list[tuple[float]]
) -> dict[tuple[float], list[tuple[float]]]:
    mapping = {tuple(ct_pt): [] for ct_pt in centers}
    for pt in vectors:
        ct_pt, _ = find_closest_center(pt, centers)
        ct_pt = tuple(ct_pt)
        mapping[ct_pt].append(pt)
    return mapping


def k_centers_farthest_first_traversal(
        k: int,
        vectors: list[tuple[float]],
        dims: int,
        iteration_callback: Callable[  # callback func to invoke on each iteration
            [
                dict[tuple[float], list[tuple[float]]]
            ],
            None
        ] | None = None
) -> dict[tuple[float], list[tuple[float]]]:
    # choose an initial center
    centers = [random.choice(vectors)]
    # notify of cluster for first iteration
    mapping = centers_to_clusters(centers, vectors)
    iteration_callback(mapping)
    # iterate
    while len(centers) < k:
        # get next center
        dists = {}
        for pt in vectors:
            _, d = find_closest_center(pt, centers)
            pt = tuple(pt)
            dists[pt] = d
        farthest_closest_center_pt = max(dists, key=lambda x: dists[x])
        centers.append(farthest_closest_center_pt)
        # notify of the current iteration's cluster
        mapping = centers_to_clusters(centers, vectors)
        iteration_callback(mapping)
    return mapping
```