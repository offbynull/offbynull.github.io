from __future__ import annotations

import colorsys
from itertools import product
from random import random, Random
from sys import stdin
from typing import Callable, Iterable

import yaml

from ch7_copy.distance_matrix.DistanceMatrix import DistanceMatrix
from ch7_copy.phylogeny.NeighbourJoiningPhylogeny import neighbour_joining_phylogeny
from ch7_copy.phylogeny.TreeToAdditiveDistanceMatrix import find_path
from clustering.Soft_HierarchialClustering_NeighbourJoining import get_leaf_distances
from graph.UndirectedGraph import Graph
from metrics.CosineSimilarity import cosine_distance
from metrics.EuclideanDistance import euclidean_distance
from metrics.ManhattanDistance import manhattan_distance
from metrics.PearsonSimilarity import pearson_distance


def _get_colors(num_colors):
    r = Random(0)
    colors=[]
    step = 360.0 / num_colors
    for i in range(0, num_colors):
        hue = (step * i) / 360.0
        lightness = (50 + r.random() * 10) / 100.0
        saturation = (90 + r.random() * 10) / 100.0
        rgb_floats = colorsys.hls_to_rgb(hue, lightness, saturation)
        rgb_hex = '#' + ''.join(f'{int(255 * f):02x}' for f in rgb_floats)
        colors.append(rgb_hex)
    return colors


def to_dot(g: Graph, clusters: Clusters, edge_scale=1.0) -> str:
    colors = _get_colors(len(clusters))
    ret = 'graph G {\n'
    ret += ' layout=neato\n'
    ret += ' node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = sorted(g.get_nodes())
    for n in nodes:
        ret += f'{n}'
        for i, cluster in enumerate(clusters):
            if n in cluster:
                ret += f' [style=filled, fillcolor="{colors[i]}"]'
                break
        ret += '\n'
    for e in sorted(g.get_edges()):
        n1, n2, weight = g.get_edge(e)
        ret += f'{n1} -- {n2} [label="{weight:.2f}", len={(weight * edge_scale):.10f}]\n'
    ret += '}'
    return ret





















# MARKDOWN_DISTORTED_AVG
# Distorted avg -- like avg, but reduces the influence of outliers. The larger e is, the
# less influence the outlier will have.
def distorted_avg(values: list[float], e: float) -> float:
    count = len(values)
    return (sum(v ** (1 / e) for v in values) / count) ** e
# MARKDOWN_DISTORTED_AVG


# MARKDOWN_ESTIMATE_OWNERSHIP
def estimate_ownership(
        tree: Graph[str, None, str, float],
        dist_mat: DistanceMatrix[str],
        davg_exp: float = 2.0,
        davg_scale: float = 1.0
) -> tuple[dict[str, str], dict[str, str]]:
    # Calculate distorted average of edge weights/distances.
    #   WARNING: Neighbour joining phylogeny sometimes produces edges with
    #   miniscule or negative weights when the distance matrix isn't an
    #   additive matrix. These should be de-noised before calling this
    #   function (e.g. nodes at ends of miniscule/negative edges should be
    #   merged) because they'll throw off this heuristic metric
    dists = [tree.get_edge_data(e) for e in tree.get_edges()]
    davg_dist = distorted_avg(dists, davg_exp)
    davg_dist_scaled = davg_dist * davg_scale
    # Assign leaf nodes to each internal node based on distance. That distance
    # is compared against the distorted average to determine assignment.
    #
    # The same leaf node may be assigned to multiple different internal nodes.
    internal_to_leaves = {}
    leaves_to_internal = {}
    internal_nodes = {n for n in tree.get_nodes() if tree.get_degree(n) > 1}
    for n_i in internal_nodes:
        leaf_dists = get_leaf_distances(tree, n_i)
        for n_l, dist in leaf_dists.items():
            if dist > davg_dist_scaled:
                continue
            internal_to_leaves.setdefault(n_i, set()).add(n_l)
            leaves_to_internal.setdefault(n_l, set()).add(n_i)
    # Return assignments
    return internal_to_leaves, leaves_to_internal
# MARKDOWN_ESTIMATE_OWNERSHIP


# MARKDOWN_MERGE_OVERLAPS
def merge_overlaps(
        n_leaf: str,
        internal_to_leaves: dict[str, str],
        leaves_to_internal: dict[str, str]
):
    prev_n_leaves_len = 0
    prev_n_internals_len = 0
    n_leaves = {n_leaf}
    n_internals = {}
    while prev_n_internals_len != len(n_internals) or prev_n_leaves_len != len(n_leaves):
        prev_n_internals_len = len(n_internals)
        prev_n_leaves_len = len(n_leaves)
        n_internals = {n_i for n_l in n_leaves for n_i in leaves_to_internal[n_l]}
        n_leaves = {n_l for n_i in n_internals for n_l in internal_to_leaves[n_i]}
    return n_leaves, n_internals
# MARKDOWN_MERGE_OVERLAPS







DistanceMetric = Callable[[tuple[float, ...], tuple[float, ...], int], float]
Clusters = list[set[str]]


# MARKDOWN
def soft_hierarchial_clustering_neighbour_joining(
        vectors: dict[str, tuple[float, ...]],
        dims: int,
        distance_metric: DistanceMetric,
        gen_node_id: Callable[[], str],
        gen_edge_id: Callable[[], str],
        davg_exp: float = 2.0,
        davg_scale: float = 1.0
) -> tuple[
    DistanceMatrix[str],
    Graph[str, None, str, float],
    Clusters
]:
    # Generate a distance matrix from the vectors
    dists = {}
    for (k1, v1), (k2, v2) in product(vectors.items(), repeat=2):
        if k1 == k2:
            continue  # skip -- will default to 0
        dists[k1, k2] = distance_metric(v1, v2, dims)
    dist_mat = DistanceMatrix(dists)
    # Run neighbour joining phylogeny on the distance matrix
    tree = neighbour_joining_phylogeny(dist_mat, gen_node_id, gen_edge_id)
    # Find clusters by estimating which internal node owns which leaf node (there may be multiple
    # estimated owners), then merge overlapping estimates.
    # then merging together overlapping owners.
    internal_to_leaves, leaves_to_internal = estimate_ownership(tree, dist_mat, davg_exp=davg_exp, davg_scale=davg_scale)
    clusters = []
    while len(leaves_to_internal) > 0:
        n_leaf = next(iter(leaves_to_internal))
        n_leaves, n_internals = merge_overlaps(n_leaf, internal_to_leaves, leaves_to_internal)
        for n in n_internals:
            del internal_to_leaves[n]
        for n in n_leaves:
            del leaves_to_internal[n]
        if len(n_leaves) > 1:  # cluster of 1 is not a cluster
            clusters.append(n_leaves | n_internals)
    # Return
    return dist_mat, tree, clusters
# MARKDOWN





def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = stdin.read()
        data: dict = yaml.safe_load(data_raw)
        vectors = {k: tuple(v) for k, v in data['vectors'].items()}
        metric = data['metric']
        edge_scale = data.get('edge_scale', default=1.0)
        dims = max(len(v) for v in vectors.values())
        print(f'Executing neighbour joining phylogeny **soft** clustering using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        metric_func = {
            'euclidean': euclidean_distance,
            'manhattan': manhattan_distance,
            'cosine': cosine_distance,
            'pearson': pearson_distance
        }[metric]
        _next_edge_id = 0
        def gen_edge_id():
            nonlocal _next_edge_id
            _next_edge_id += 1
            return f'E{_next_edge_id}'
        _next_node_id = 0
        def gen_node_id():
            nonlocal _next_node_id
            _next_node_id += 1
            return f'N{_next_node_id}'
        dist_mat, tree, clusters = soft_hierarchial_clustering_neighbour_joining(vectors, dims, metric_func, gen_node_id, gen_edge_id)
        print('The following distance matrix was produced ...')
        print()
        print('<table>')
        print('<thead><tr>')
        print('<th></th>')
        for l in sorted(dist_mat.leaf_ids_it()):
            print(f'<th>{l}</th>')
        print('</tr></thead>')
        print('<tbody>')
        for l1 in sorted(dist_mat.leaf_ids_it()):
            print('<tr>')
            print(f'<td>{l1}</td>')
            for l2 in sorted(dist_mat.leaf_ids_it()):
                print(f'<td>{dist_mat[l1, l2]:.2f}</td>')
            print('</tr>')
        print('</tbody>')
        print('</table>')
        print()
        print(f'The following neighbour joining phylogeny tree was produced ...')
        print()
        print('```{dot}')
        print(f'{to_dot(tree, clusters, edge_scale)}')
        print('```')
        print()
        print(f'The following clusters were estimated ...')
        print()
        for nodes in clusters:
            print(f' * {", ".join(nodes)}')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()