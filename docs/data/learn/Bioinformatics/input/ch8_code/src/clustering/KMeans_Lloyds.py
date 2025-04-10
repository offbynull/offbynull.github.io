from __future__ import annotations

import itertools
import random
from math import dist
from pathlib import Path
from statistics import mean
from sys import stdin
from typing import Optional, Callable

import matplotlib.pyplot as plt
import yaml


def plot_2d(
        clusters: dict[tuple[float], list[tuple[float]]],
        output_path: Optional[Path]
) -> None:
    plt.close() # reset
    cm = plt.cm.get_cmap('hsv', len(clusters) + 1)
    cluster_colors = {center: cm(i) for i, center in enumerate(clusters)}
    xs = []
    ys = []
    colors = []
    markers = []
    sizes = []
    for center in clusters:
        xs.append(center[0])
        ys.append(center[1])
        colors.append('black')
        markers.append('x')
        sizes.append(160)
        color = cluster_colors[center]
        for pt in clusters[center]:
            xs.append(pt[0])
            ys.append(pt[1])
            colors.append(color)
            markers.append('o')
            sizes.append(40)
    group_by_markers = itertools.groupby(zip(markers, colors, sizes, xs, ys), key=lambda x: x[0])
    for marker, group in group_by_markers:
        group = list(group)
        group_xs = [e[3] for e in group]
        group_ys = [e[4] for e in group]
        group_colors = [e[1] for e in group]
        group_sizes = [e[2] for e in group]
        plt.scatter(group_xs, group_ys, color=group_colors, marker=marker, s=group_sizes)
    if output_path is not None:
        plt.savefig(output_path)
    else:
        plt.show()


def plot_3d(
        clusters: dict[tuple[float], list[tuple[float]]],
        output_path: Optional[Path]
) -> None:
    plt.close() # reset
    cm = plt.cm.get_cmap('hsv', len(clusters) + 1)
    cluster_colors = {center: cm(i) for i, center in enumerate(clusters)}
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    xs = []
    ys = []
    zs = []
    colors = []
    markers = []
    sizes = []
    for center in clusters:
        xs.append(center[0])
        ys.append(center[1])
        zs.append(center[2])
        colors.append('black')
        markers.append('x')
        sizes.append(160)
        color = cluster_colors[center]
        for pt in clusters[center]:
            xs.append(pt[0])
            ys.append(pt[1])
            zs.append(pt[2])
            colors.append(color)
            sizes.append(40)
            markers.append('o')
    group_by_markers = itertools.groupby(zip(markers, colors, sizes, xs, ys, zs), key=lambda x: x[0])
    for marker, group in group_by_markers:
        group = list(group)
        group_xs = [e[3] for e in group]
        group_ys = [e[4] for e in group]
        group_zs = [e[5] for e in group]
        group_colors = [e[1] for e in group]
        group_sizes = [e[2] for e in group]
        ax.scatter(group_xs, group_ys, group_zs, color=group_colors, marker=marker, s=group_sizes)
    if output_path is not None:
        plt.savefig(output_path)
    else:
        plt.show()





















# MARKDOWN_CLOSEST_CENTER
def find_closest_center(
        point: tuple[float],
        centers: list[tuple[float]],
) -> tuple[tuple[float], float]:
    center = min(
        centers,
        key=lambda cp: dist(point, cp)
    )
    return center, dist(center, point)
# MARKDOWN_CLOSEST_CENTER


# MARKDOWN_CENTER_OF_GRAVITY
def center_of_gravity(
        points: list[tuple[float]],
        dims: int
) -> tuple[float]:
    center = []
    for i in range(dims):
        val = mean(pt[i] for pt in points)
        center.append(val)
    return tuple(center)
# MARKDOWN_CENTER_OF_GRAVITY


MembershipAssignmentMap = dict[tuple[float], list[tuple[float]]]
IterationCallbackFunc = Callable[[MembershipAssignmentMap], None]

# MARKDOWN
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
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data = yaml.safe_load(stdin)
        k = data[0]
        vectors = [tuple(v) for v in data[1]]
        if len(data) > 2:
            centers = [tuple(v) for v in data[2]]
        else:
            centers = tuple(random.sample(vectors, k))
        assert len(centers) == k, 'k must match number of centers'
        dims = max(len(v) for v in vectors)
        print(f'Given {k=} and {vectors=}...')
        print()
        print(f'The llyod\'s algorithm heuristic produced the clusters at each iteration ...')
        print()
        unique_id_path = Path('/input/.__UNIQUE_INPUT_ID')
        iteration = 0
        def plot_iteration(clusters):
            nonlocal iteration
            plot_path = None
            if unique_id_path.exists():
                unique_id = unique_id_path.read_text()
                plot_path = Path(f'/output/{unique_id}_plot{iteration}.svg')
            print(f' * Iteration {iteration}')
            print()
            for center in clusters:
                print(f'    * cluster center {center}={clusters[center]}')
            print()
            if dims == 2:
                plot_2d(clusters, plot_path)
                print(f'   ![k-means 2D plot]({None if plot_path is None else plot_path.name})')
                print()
            elif dims == 3:
                plot_3d(clusters, plot_path)
                print(f'   ![k-means 3D plot]({None if plot_path is None else plot_path.name})')
                print()
            else:
                print(f"   Unable to plot iteration -- too many dimensions")
                print()
            iteration += 1
        k_means_lloyds(k, vectors, centers, dims, plot_iteration)
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")



























# MARKDOWN_KMEANS_PP_INITIALIZER
def k_means_PP_initializer(
        k: int,
        vectors: list[tuple[float]],
):
    centers = [random.choice(vectors)]
    while len(centers) < k:
        choice_points = []
        choice_weights = []
        for v in vectors:
            if v in centers:
                continue
            _, d = find_closest_center(v, centers)
            choice_weights.append(d)
            choice_points.append(v)
        total = sum(choice_weights)
        choice_weights = [w / total for w in choice_weights]
        c_pt = random.choices(choice_points, weights=choice_weights, k=1).pop(0)
        centers.append(c_pt)
    return centers
# MARKDOWN_KMEANS_PP_INITIALIZER


def main_WITH_k_means_PP_initializer():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data = yaml.safe_load(stdin)
        k = data[0]
        vectors = [tuple(v) for v in data[1]]
        dims = max(len(v) for v in vectors)
        print(f'Given {k=} and {vectors=}...')
        print()
        print(f'The llyod\'s algorithm heuristic produced the clusters at each iteration ...')
        print()
        unique_id_path = Path('/input/.__UNIQUE_INPUT_ID')
        iteration = 0
        def plot_iteration(clusters):
            nonlocal iteration
            plot_path = None
            if unique_id_path.exists():
                unique_id = unique_id_path.read_text()
                plot_path = Path(f'/output/{unique_id}_plot{iteration}.svg')
            print(f' * Iteration {iteration}')
            print()
            for center in clusters:
                print(f'    * cluster center {center}={clusters[center]}')
            print()
            if dims == 2:
                plot_2d(clusters, plot_path)
                print(f'   ![k-means 2D plot]({None if plot_path is None else plot_path.name})')
                print()
            elif dims == 3:
                plot_3d(clusters, plot_path)
                print(f'   ![k-means 3D plot]({None if plot_path is None else plot_path.name})')
                print()
            else:
                print(f"   Unable to plot iteration -- too many dimensions")
                print()
            iteration += 1
        k_means_lloyds(k, vectors, k_means_PP_initializer(k, vectors), dims, plot_iteration)
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


























if __name__ == '__main__':
    main()

