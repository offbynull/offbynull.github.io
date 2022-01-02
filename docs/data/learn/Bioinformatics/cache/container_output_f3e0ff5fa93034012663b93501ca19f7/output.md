`{bm-disable-all}`[ch8_code/src/clustering/KCenters_FarthestFirstTraversal.py](ch8_code/src/clustering/KCenters_FarthestFirstTraversal.py) (lines 11 to 54):`{bm-enable-all}`

```python
def distance_to_closest_center(
        v: Sequence[float],
        centers: list[Sequence[float]]
) -> tuple[Sequence[float], float]:
    return min(
        ((c, dist(v, c)) for c in centers),
        key=lambda x: x[1]
    )


def pick_centers(
        k: int,
        vectors: list[Sequence[float]],
        dims: int
) -> list[Sequence[float]]:
    centers = [random.choice(vectors)]
    while len(centers) < k:
        # For each vector, find the distance to its closest center
        dists = {}
        for v in vectors:
            _, d = distance_to_closest_center(v, centers)
            v = tuple(v)  # Dict requires hashable keys
            dists[v] = d
        # Of all the "closest distance"s found above, get the
        # vector with the largest one (farthest closest center)
        v_with_max_closest_center_dist = max(dists, key=lambda x: dists[x])
        # Add that vector as a center
        centers.append(v_with_max_closest_center_dist)
    return centers


def k_centers(
        k: int,
        vectors: list[Sequence[float]],
        dims: int
) -> list[Sequence[list]]:
    centers = pick_centers(k, vectors, dims)
    clusters = defaultdict(list)
    for v in vectors:
        center, _ = distance_to_closest_center(v, centers)
        center = tuple(center)  # Dict requires hashable keys
        clusters[center].append(v)
    return list(clusters.values())
```