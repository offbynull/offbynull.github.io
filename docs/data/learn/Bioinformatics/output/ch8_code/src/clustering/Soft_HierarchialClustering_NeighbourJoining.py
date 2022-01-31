from __future__ import annotations

from itertools import product
from sys import stdin
from typing import Callable

import yaml

from ch7_copy.distance_matrix.DistanceMatrix import DistanceMatrix
from ch7_copy.phylogeny.NeighbourJoiningPhylogeny import neighbour_joining_phylogeny
from graph.UndirectedGraph import Graph
from metrics.CosineSimilarity import cosine_distance
from metrics.EuclideanDistance import euclidean_distance
from metrics.ManhattanDistance import manhattan_distance
from metrics.PearsonSimilarity import pearson_distance


def to_dot(g: Graph) -> str:
    ret = 'graph G {\n'
    ret += ' layout=neato\n'
    ret += ' node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = sorted(g.get_nodes())
    for n in nodes:
        ret += f'{n}\n'
    for e in sorted(g.get_edges()):
        n1, n2, weight = g.get_edge(e)
        ret += f'{n1} -- {n2} [label="{weight:.2f}", len={weight:.2f}]\n'
    ret += '}'
    return ret









# MARKDOWN_LEAF_NODE_DISTANCES
def get_leaf_distances(
        tree: Graph[str, None, str, float],
        n: str,
        from_n: str | None,
        from_dist: float,
        dists: dict[str, float]
) -> None:
    # Find neighbours of n (that aren't from_n)
    n_neighbours = []
    edges = set(tree.get_outputs(n))
    for e in edges:
        n_other = tree.get_edge_end(e, n)
        if from_n is not None and n_other == from_n:
            continue
        n_neighbours.append((n_other, e))
    # No neighbours? It's a leaf node -- set the dist and leave.
    if len(n_neighbours) == 0:
        dists[n] = from_dist
        return
    # Otherwise, walk to each neighbour.
    for n_other, e in n_neighbours:
        e_dist = tree.get_edge_data(e)
        get_leaf_distances(tree, n_other, n, from_dist + e_dist, dists)
# MARKDOWN_LEAF_NODE_DISTANCES


# MARKDOWN_PROBABILITY
def leaf_probabilities(
        tree: Graph[str, None, str, float],
        n: str,
) -> dict[str, float]:
    # Get dists between n and each to leaf node
    dists = {}
    get_leaf_distances(tree, n, None, 0.0, dists)
    # Calculate inverse distance weighting
    #   See: https://stackoverflow.com/a/23524954
    #   The link talks about a "stiffness" parameter similar to the stiffness parameter in the
    #   partition function used for soft k-means clustering. In this case, you can make the
    #   probabilities more decisive by taking the the distance to the power of X, where larger
    #   X values give more decisive probabilities.
    inverse_dists = {leaf: 1.0/d for leaf, d in dists.items()}
    inverse_dists_total = sum(inverse_dists.values())
    return {leaf: inv_dist / inverse_dists_total for leaf, inv_dist in inverse_dists.items()}
# MARKDOWN_PROBABILITY


DistanceMetric = Callable[[tuple[float], tuple[float], int], float]
ProbabilityMap = dict[str, dict[str, float]]


# MARKDOWN
def soft_hierarchial_clustering_neighbour_joining(
        vectors: dict[str, tuple[float]],
        dims: int,
        distance_metric: DistanceMetric,
        gen_node_id: Callable[[], str],
        gen_edge_id: Callable[[], str]
) -> tuple[DistanceMatrix, Graph, ProbabilityMap]:
    # Generate a distance matrix from the vectors
    dists = {}
    for (k1, v1), (k2, v2) in product(vectors.items(), repeat=2):
        if k1 == k2:
            continue  # skip -- will default to 0
        dists[k1, k2] = distance_metric(v1, v2, dims)
    dist_mat = DistanceMatrix(dists)
    # Run neighbour joining phylogeny on the distance matrix
    tree = neighbour_joining_phylogeny(dist_mat, gen_node_id, gen_edge_id)
    # Compute leaf probabilities per internal node
    internal_nodes = [n for n in tree.get_nodes() if tree.get_degree(n) > 1]
    internal_node_probs = {}
    for n_i in internal_nodes:
        internal_node_probs[n_i] = leaf_probabilities(tree, n_i)
    # Return
    return dist_mat, tree, internal_node_probs
# MARKDOWN





def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = stdin.read()
        data: dict = yaml.safe_load(data_raw)
        vectors = {k: tuple(v) for k, v in data['vectors'].items()}
        metric = data['metric']
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
        dist_mat, tree, probabilities = soft_hierarchial_clustering_neighbour_joining(vectors, dims, metric_func, gen_node_id, gen_edge_id)
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
        print(f'{to_dot(tree)}')
        print('```')
        print()
        print(f'The following leaf node membership probabilities were produced (per internal node) ...')
        print()
        for n_int, probs in probabilities.items():
            probs_str = ','.join(f'{n_leaf}={probs[n_leaf]:.2f}' for n_leaf in sorted(probs))
            print(f' * {n_int} = {probs_str}')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()