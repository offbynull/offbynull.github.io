import random
from collections import defaultdict
from math import dist
from sys import stdin
from typing import Sequence

import yaml


# MARKDOWN
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
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data = yaml.safe_load(stdin)
        k = data[0]
        vectors = data[1]
        dims = max(len(v) for v in vectors)
        print(f'Given {k=} and {vectors=}...')
        print()
        clusters = k_centers(k, vectors, dims)
        print(f'The farthest first travel heuristic produced the clusters ...')
        print()
        for i in range(k):
            print(f' * cluster {i}={clusters[i]}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()

