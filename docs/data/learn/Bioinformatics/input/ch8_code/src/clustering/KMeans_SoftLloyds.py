from __future__ import annotations

import itertools
from collections import defaultdict
from math import dist, e
from pathlib import Path
from sys import stdin
from typing import Optional, Callable

import matplotlib.pyplot as plt
import yaml

from clustering.KMeans_Lloyds import k_means_PP_initializer


def plot_2d(
        membership_confidences: dict[tuple[float], dict[tuple[float], float]],
        output_path: Optional[Path]
) -> None:
    plt.close() # reset
    xs = []
    ys = []
    markers = []
    sizes = []
    point_labels = defaultdict(str)
    center_labels = defaultdict(str)
    for c_idx, c_pt in enumerate(membership_confidences):
        xs.append(c_pt[0])
        ys.append(c_pt[1])
        markers.append('x')
        sizes.append(160)
        center_labels[c_pt] = f'{c_idx}'
        for pt in membership_confidences[c_pt]:
            xs.append(pt[0])
            ys.append(pt[1])
            markers.append('o')
            sizes.append(40)
            point_labels[pt] = f'{point_labels[pt]}\n{c_idx}={membership_confidences[c_pt][pt]:.2f}'
    group_by_markers = itertools.groupby(zip(markers, sizes, xs, ys), key=lambda x: x[0])
    for marker, group in group_by_markers:
        group = list(group)
        group_xs = [e[2] for e in group]
        group_ys = [e[3] for e in group]
        group_sizes = [e[1] for e in group]
        plt.scatter(group_xs, group_ys, marker=marker, s=group_sizes)
    for pt, text in list(point_labels.items()) + list(center_labels.items()):
        plt.annotate(text,  # this is the text
                     (pt[0], pt[1]),  # these are the coordinates to position the label
                     textcoords="offset points",  # how to position the text
                     xytext=(0, 10),  # distance from text to points (x,y)
                     ha='center')
    if output_path is not None:
        plt.savefig(output_path)
    else:
        plt.show()


def plot_3d(
        membership_confidences: dict[tuple[float], dict[tuple[float], float]],
        output_path: Optional[Path]
) -> None:
    plt.close() # reset
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    xs = []
    ys = []
    zs = []
    markers = []
    sizes = []
    point_labels = defaultdict(str)
    center_labels = defaultdict(str)
    for c_idx, c_pt in enumerate(membership_confidences):
        xs.append(c_pt[0])
        ys.append(c_pt[1])
        zs.append(c_pt[2])
        markers.append('x')
        sizes.append(160)
        center_labels[c_pt] = f'{c_idx}'
        for pt in membership_confidences[c_pt]:
            xs.append(pt[0])
            ys.append(pt[1])
            zs.append(pt[2])
            sizes.append(40)
            markers.append('o')
            point_labels[pt] = f'{point_labels[pt]}\n{c_idx}={membership_confidences[c_pt][pt]:.2f}'
    group_by_markers = itertools.groupby(zip(markers, sizes, xs, ys, zs), key=lambda x: x[0])
    for marker, group in group_by_markers:
        group = list(group)
        group_xs = [e[2] for e in group]
        group_ys = [e[3] for e in group]
        group_zs = [e[4] for e in group]
        group_sizes = [e[1] for e in group]
        ax.scatter(group_xs, group_ys, group_zs, marker=marker, s=group_sizes)
    for pt, text in list(point_labels.items()) + list(center_labels.items()):
        ax.text(pt[0], pt[1], pt[2],  # these are the coordinates to position the label
                text,  # this is the text
                # textcoords="offset points",  # how to position the text
                # xyztext=(0, 10, 0),  # distance from text to points (x,y)
                # ha='center'
                )
    if output_path is not None:
        plt.savefig(output_path)
    else:
        plt.show()














MembershipConfidenceMap = dict[
        tuple[float],  # center
        dict[          # dict of (point -> confidence_level) for center
            tuple[float],
            float
        ]
]


# MARKDOWN_E_STEP
# For each center, estimate the confidence of point belonging to that center using the partition
# function from statistical physics.
#
# What is the partition function's stiffness parameter? You can thnk of stiffness as how willing
# the partition function is to be polarizing. For example, if you set stiffness to 1.0, whichever
# center the point teeters towards will have maximum confidence (1) while all other centers will
# have no confidence (0).
def confidence(
        point: tuple[float],
        centers: list[tuple[float]],
        stiffness: float
) -> dict[tuple[float], float]:
    confidences = {}
    total = 0
    for c in centers:
        total += e ** (-stiffness * dist(point, c))
    for c in centers:
        val = e ** (-stiffness * dist(point, c))
        confidences[c] = val / total
    return confidences  # center -> confidence value


# E-STEP: For each data point, estimate the confidence level of it belonging to each of the
# centers.
def e_step(
        points: list[tuple[float]],
        centers: list[tuple[float]],
        stiffness: float
) -> MembershipConfidenceMap:
    membership_confidence = {c: {} for c in centers}
    for pt in points:
        pt_confidences = confidence(pt, centers, stiffness)
        for c, val in pt_confidences.items():
            membership_confidence[c][pt] = val
    return membership_confidence  # confidence per (center, point) pair
# MARKDOWN_E_STEP


# MARKDOWN_M_STEP
def weighted_center_of_gravity(
        confidence_set: dict[tuple[float], float],
        dims: int
) -> tuple[float]:
    center: list[float] = []
    all_confidences = confidence_set.values()
    all_confidences_summed = sum(all_confidences)
    for i in range(dims):
        val = 0.0
        for pt, confidence in confidence_set.items():
            val += pt[i] * confidence  # scale by confidence
        val /= all_confidences_summed
        center.append(val)
    return tuple(center)


# M-STEP: Calculate a new set of centers from the "confidence levels" derived in the E-step.
def m_step(
        membership_confidences: MembershipConfidenceMap,
        dims: int
) -> list[tuple[float]]:
    centers = []
    for c in membership_confidences:
        new_c = weighted_center_of_gravity(
            membership_confidences[c],
            dims
        )
        centers.append(new_c)
    return centers
# MARKDOWN_M_STEP


IterationCallbackFunc = Callable[[MembershipConfidenceMap], bool]

# MARKDOWN
def k_means_soft_lloyds(
        k: int,
        points: list[tuple[float]],
        centers_init: list[tuple[float]],
        dims: int,
        stiffness: float,
        iteration_callback: IterationCallbackFunc
) -> MembershipConfidenceMap:
    centers = centers_init[:]
    while True:
        membership_confidences = e_step(points, centers, stiffness)  # step1: centers to clusters (E-step)
        centers = m_step(membership_confidences, dims)               # step2: clusters to centers (M-step)
        # check to see if you can stop iterating ("converged" enough to stop)
        continue_flag = iteration_callback(membership_confidences)
        if not continue_flag:
            break
    return membership_confidences
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = stdin.read()
        data: dict = yaml.safe_load(data_raw)
        k = data['k']
        vectors = [tuple(pt) for pt in data['points']]
        stiffness = data['stiffness']
        show_every = data['show_every']
        stop_instructions = data['stop_instructions']
        centers = data.get('centers', None)
        if centers is not None:
            centers = [tuple(c) for c in centers]
            assert len(centers) == k, 'k must match number of centers'
        else:
            centers = k_means_PP_initializer(k, vectors)
        dims = max(len(v) for v in vectors)
        print()
        print(f'Executing soft llyod\'s algorithm heuristic using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        unique_id_path = Path('/input/.__UNIQUE_INPUT_ID')
        def print_cluster(clusters):
            plot_path = None
            if unique_id_path.exists():
                unique_id = unique_id_path.read_text()
                plot_path = Path(f'/output/{unique_id}_plot{iteration}.svg')
            for center in clusters:
                print(f'    * cluster center {center}={{{", ".join(f"{p}: {conf:.2f}" for p, conf in clusters[center].items())}}}')
            print()
            if dims == 2:
                plot_2d(clusters, plot_path)
                print(f'    ![k-centers 2D plot]({None if plot_path is None else plot_path.name})')
                print()
            elif dims == 3:
                plot_3d(clusters, plot_path)
                print(f'    ![k-centers 3D plot]({None if plot_path is None else plot_path.name})')
                print()
            else:
                print(f"    Unable to plot iteration -- too many dimensions")
                print()
        iteration = 0
        prev_clusters = None
        def plot_iteration(clusters):
            nonlocal iteration
            nonlocal prev_clusters
            if iteration % show_every == 0:
                print(f' * Iteration {iteration}')
                print()
                print_cluster(clusters)
            if stop_instructions['max_iterations'] <= iteration:
                print(f'Stopping -- hit max iterations ({iteration=})')
                print()
                return False
            if prev_clusters is not None:
                largest_center_step_distance = max(dist(c_new, c_old) for c_new, c_old in zip(clusters, prev_clusters))
                if stop_instructions['min_center_step_distance'] > largest_center_step_distance:
                    print(f'Stopping -- center convergence step distance below threshold ({largest_center_step_distance=})')
                    print()
                    return False
            iteration += 1
            prev_clusters = clusters
            return True
        final_clusters = k_means_soft_lloyds(k, vectors, centers, dims, stiffness, plot_iteration)
        print(" * FINAL RESULT:")
        print()
        print_cluster(final_clusters)
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()

