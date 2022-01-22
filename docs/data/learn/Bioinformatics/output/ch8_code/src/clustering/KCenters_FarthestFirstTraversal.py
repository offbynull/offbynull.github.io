from __future__ import annotations

import itertools
import random
from math import dist
from pathlib import Path
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
        sizes.append(80)
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
        sizes.append(80)
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





















# MARKDOWN
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
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data = yaml.safe_load(stdin)
        k = data[0]
        vectors = [tuple(v) for v in data[1]]
        dims = max(len(v) for v in vectors)
        print(f'Given {k=} and {vectors=}...')
        print()
        print(f'The farthest first travel heuristic produced the clusters at each iteration ...')
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
                print(f'   ![k-centers 2D plot]({None if plot_path is None else plot_path.name})')
                print()
            elif dims == 3:
                plot_3d(clusters, plot_path)
                print(f'   ![k-centers 3D plot]({None if plot_path is None else plot_path.name})')
                print()
            else:
                print(f"   Unable to plot iteration -- too many dimensions")
                print()
            iteration += 1
        clusters = k_centers_farthest_first_traversal(k, vectors, dims, plot_iteration)
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()

