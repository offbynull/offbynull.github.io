import itertools
import random
from collections import defaultdict
from math import dist
from pathlib import Path
from sys import stdin
from typing import Sequence, Optional

import matplotlib.pyplot as plt
import yaml


def plot_2d(
        clusters: dict[tuple[float], list[Sequence[float]]],
        output_path: Optional[Path]
) -> None:
    cm = plt.cm.get_cmap('hsv', len(clusters) + 1)
    cluster_colors = {center: cm(i) for i, center in enumerate(clusters)}
    xs = []
    ys = []
    colors = []
    markers = []
    for center in clusters:
        color = cluster_colors[center]
        for pt in clusters[center]:
            xs.append(pt[0])
            ys.append(pt[1])
            colors.append(color)
            markers.append('d' if tuple(pt) == center else 'o')
    group_by_markers = itertools.groupby(zip(markers, colors, xs, ys), key=lambda x: x[0])
    for marker, group in group_by_markers:
        group = list(group)
        group_xs = [e[2] for e in group]
        group_ys = [e[3] for e in group]
        group_colors = [e[1] for e in group]
        plt.scatter(group_xs, group_ys, color=group_colors, marker=marker)
    if output_path is not None:
        plt.savefig(output_path)
    else:
        plt.show()


def plot_3d(
        clusters: dict[tuple[float], list[Sequence[float]]],
        output_path: Optional[Path]
) -> None:
    cm = plt.cm.get_cmap('hsv', len(clusters) + 1)
    cluster_colors = {center: cm(i) for i, center in enumerate(clusters)}
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    xs = []
    ys = []
    zs = []
    colors = []
    markers = []
    for center in clusters:
        color = cluster_colors[center]
        for pt in clusters[center]:
            xs.append(pt[0])
            ys.append(pt[1])
            zs.append(pt[2])
            colors.append(color)
            markers.append('d' if tuple(pt) == center else 'o')
    group_by_markers = itertools.groupby(zip(markers, colors, xs, ys, zs), key=lambda x: x[0])
    for marker, group in group_by_markers:
        group = list(group)
        group_xs = [e[2] for e in group]
        group_ys = [e[3] for e in group]
        group_zs = [e[4] for e in group]
        group_colors = [e[1] for e in group]
        ax.scatter(group_xs, group_ys, group_zs, color=group_colors, marker=marker)
    if output_path is not None:
        plt.savefig(output_path)
    else:
        plt.show()





















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
) -> dict[tuple[float], list[Sequence[float]]]:
    centers = pick_centers(k, vectors, dims)
    clusters = defaultdict(list)
    for v in vectors:
        center, _ = distance_to_closest_center(v, centers)
        center = tuple(center)  # Dict requires hashable keys
        clusters[center].append(v)
    return clusters
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
        for center in clusters:
            print(f' * cluster center {center}={clusters[center]}')
        print()
        unique_id_path = Path('/input/.__UNIQUE_INPUT_ID')
        plot_path = None
        if unique_id_path.exists():
            unique_id = unique_id_path.read_text()
            plot_path = Path(f'/output/{unique_id}_plot.svg')
        if dims == 2:
            plot_2d(clusters, plot_path)
            print(f'![k-centers 2D plot]({plot_path.name})')
            print()
            print('Note: Each cluster is its own color, a point that\'s diamond shaped is the centers for its clusters')
        elif dims == 3:
            plot_3d(clusters, plot_path)
            print(f'![k-centers 3D plot]({plot_path.name})')
            print()
            print('Note: Each cluster is its own color, a point that\'s diamond shaped is the centers for its clusters')
        else:
            print("Unable to plot -- too many dimensions")
            print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()

