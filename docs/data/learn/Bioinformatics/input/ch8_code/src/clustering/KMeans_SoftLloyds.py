from __future__ import annotations

import itertools
import random
from collections import defaultdict
from math import dist, nan, e
from pathlib import Path
from statistics import mean
from sys import stdin
from typing import Sequence, Optional, Callable

import matplotlib.pyplot as plt
import yaml


def plot_2d(
        clusters: dict[tuple[float], list[Sequence[float]]],
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
        clusters: dict[tuple[float], list[Sequence[float]]],
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















def dot_product(a, b):
    return sum(e_a * e_b for e_a, e_b in zip(a, b))


# MARKDOWN_PARTITION_FUNC
def partition_function(
        point: tuple[float],
        center_pts: list[tuple[float]],
        stiffness: float
):
    confidences = {}
    total_pf = 0
    for c_pt in center_pts:
        total_pf += e ** (-stiffness * dist(point, c_pt))
    for c_pt in center_pts:
        pf = e ** (-stiffness * dist(point, c_pt))
        confidences[point] = pf / total_pf
    return confidences
# MARKDOWN_PARTITION_FUNC


#   cpA and cpB -- prob of coinA and coinB to produce heads = THESE ARE THE CENTERS
#   the _outcome_ of each 10 flip round (heads ratio)       = THESE ARE THE POINTS
#   which coin was used per 10 flip round (coinA or coinB)  = THESE ARE THE CLUSTER ASSIGNMENTS

# E-step: centers to "soft" clusters
# ----------------------------------
# For each data point, estimate the confidence level that it belongs to each of the "centers". The algorithm below is
# the "partition function" from statistical physics. These confidence levels are sometimes also referred to as a
# "responsibility matrix" or "hidden matrix".
def e_step(
        data_pts: list[tuple[float]],
        center_pts: list[tuple[float]],
        stiffness: float
) -> dict[
    tuple[float],              # center point
    dict[tuple[float], float]  # data point -> confidence
]:
    membership_confidence = {c_pt: {} for c_pt in center_pts}
    for d_pt in data_pts:
        total_pf = 0
        for c_pt in center_pts:
            total_pf += e ** (-stiffness * dist(d_pt, c_pt))
        for c_pt in center_pts:
            pf = e ** (-stiffness * dist(d_pt, c_pt))
            membership_confidence[c_pt][d_pt] = pf / total_pf
    return membership_confidence


# M-step: "soft" clusters to centers
# ----------------------------------
# Calculate a new set of centers from the "confidence levels" derived in the E-step.
def m_step(
        membership_confidence: dict[tuple[float], dict[tuple[float], float]],
        dims: int
) -> list[tuple[float]]:
    centers = []
    for ct_pt in membership_confidence:
        new_ct_pt = weighted_center_of_gravity(
            membership_confidence[ct_pt],
            dims
        )
        centers.append(new_ct_pt)
    return centers


# MARKDOWN_WEIGHTED_CENTER_OF_GRAVITY
def weighted_center_of_gravity(
        confidence_set: dict[tuple[float], float],
        dims: int
) -> tuple[float]:
    center_pt: list[float] = []
    for i in range(dims):
        pt_coordinates = [pt[i] for pt in confidence_set.keys()]
        pt_confidences = confidence_set.values()
        total_confidences = sum(pt_confidences)
        ct_coordinate = dot_product(pt_coordinates, pt_confidences) / total_confidences
        center_pt.append(ct_coordinate)
    return tuple(center_pt)
# MARKDOWN_WEIGHTED_CENTER_OF_GRAVITY

x = weighted_center_of_gravity(
    {
        (1,): 0.2,
        (4,): 1,
        (5,): 1
    },
    1
)
print(f'{x}')

IterationCallback = Callable[  # callback func to invoke on each iteration
    [
        dict[tuple[float], list[tuple[tuple[float], float]]]
    ],
    None
]


# MARKDOWN
def k_means_soft_lloyds(
        k: int,
        points: list[tuple[float]],
        centers_init: list[tuple[float]],
        dims: int,
        stiffness: float = 0.5,
        iteration_callback: IterationCallback | None = None
) -> dict[
        tuple[float],  # center
        dict[          # dict of (point -> confidence_level) for center
            tuple[float],
            float
        ]
]:
    old_centers = []
    centers = centers_init[:]
    mapping = {}
    while centers != old_centers:
        # centers to clusters
        membership_confidence = e_step(points, centers, stiffness)
        # clusters to centers
        centers = m_step(membership_confidence, dims)
        # notify of current iteration's cluster
        mapping = {ct: list(zip(points, membership_confidence[ct])) for ct in centers}
        if iteration_callback is not None:
            iteration_callback(mapping)
    return mapping
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data = yaml.safe_load(stdin)
        k = data[0]
        vectors = data[1]
        if len(data) > 2:
            centers = data[2]
        else:
            centers = random.sample(vectors, k)
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
        k_means_lloyds(k, vectors, centers, dims, plot_iteration)
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")



























# MARKDOWN_KMEANS_PP_INITIALIZER
def k_means_PP_initializer(
        k: int,
        vectors: list[Sequence[float]],
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
        vectors = data[1]
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
        k_means_lloyds(k, vectors, k_means_PP_initializer(k, vectors), dims, plot_iteration)
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


























if __name__ == '__main__':
    main()

