`{bm-disable-all}`[ch8_code/src/clustering/KCenters_FarthestFirstTraversal.py](ch8_code/src/clustering/KCenters_FarthestFirstTraversal.py) (lines 120 to 167):`{bm-enable-all}`

```python
def find_closest_center(
        point: tuple[float],
        centers: list[tuple[float]],
) -> tuple[tuple[float], float]:
    center = min(
        centers,
        key=lambda cp: dist(point, cp)
    )
    return center, dist(center, point)


def centers_to_clusters(
        centers: list[tuple[float]],
        points: list[tuple[float]]
) -> MembershipAssignmentMap:
    mapping = {c: [] for c in centers}
    for pt in points:
        c, _ = find_closest_center(pt, centers)
        c = tuple(c)
        mapping[c].append(pt)
    return mapping


def k_centers_farthest_first_traversal(
        k: int,
        points: list[tuple[float]],
        dims: int,
        iteration_callback: IterationCallbackFunc
) -> MembershipAssignmentMap:
    # choose an initial center
    centers = [random.choice(points)]
    # notify of cluster for first iteration
    mapping = centers_to_clusters(centers, points)
    iteration_callback(mapping)
    # iterate
    while len(centers) < k:
        # get next center
        dists = {}
        for pt in points:
            _, d = find_closest_center(pt, centers)
            dists[pt] = d
        farthest_closest_center_pt = max(dists, key=lambda x: dists[x])
        centers.append(farthest_closest_center_pt)
        # notify of the current iteration's cluster
        mapping = centers_to_clusters(centers, points)
        iteration_callback(mapping)
    return mapping
```