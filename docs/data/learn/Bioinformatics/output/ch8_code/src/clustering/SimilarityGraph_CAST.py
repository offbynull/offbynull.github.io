from itertools import product, combinations
from statistics import mean
from sys import stdin
from typing import Callable

import yaml

from graph.UndirectedGraph import Graph
from metrics.CosineSimilarity import cosine_similarity
from metrics.EuclideanDistance import euclidean_similarity
from metrics.ManhattanDistance import manhattan_similarity
from metrics.PearsonSimilarity import pearson_similarity
from similarity_matrix.SimilarityMatrix import SimilarityMatrix


def to_dot(g: Graph) -> str:
    ret = 'graph G {\n'
    ret += ' layout=circo\n'
    ret += ' node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = sorted(g.get_nodes())
    for n in nodes:
        ret += f'{n}\n'
    for e in sorted(g.get_edges()):
        n1, n2, weight = g.get_edge(e)
        ret += f'{n1} -- {n2}\n'
    ret += '}'
    return ret














SimilarityMetric = Callable[[tuple[float, ...], tuple[float, ...], int], float]


# MARKDOWN_SIM_GRAPH
def similarity_graph(
        vectors: dict[str, tuple[float, ...]],
        dims: int,
        similarity_metric: SimilarityMetric,
        threshold: float,
) -> tuple[Graph, SimilarityMatrix]:
    # Generate similarity matrix from the vectors
    dists = {}
    for (k1, v1), (k2, v2) in product(vectors.items(), repeat=2):
        dists[k1, k2] = similarity_metric(v1, v2, dims)
    sim_mat = SimilarityMatrix(dists)
    # Generate similarity graph
    nodes = sim_mat.leaf_ids()
    sim_graph = Graph()
    for n in nodes:
        sim_graph.insert_node(n)
    for n1, n2 in product(nodes, repeat=2):
        if n1 == n2:
            continue
        e = f'E{sorted([n1, n2])}'
        if sim_graph.has_edge(e):
            continue
        if sim_mat[n1, n2] < threshold:
            continue
        sim_graph.insert_edge(e, n1, n2)
    # Return
    return sim_graph, sim_mat
# MARKDOWN_SIM_GRAPH


def main_similarity_graph():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        vectors = {k: tuple(v) for k, v in data['vectors'].items()}
        metric = data['metric']
        threshold = data['threshold']
        dims = max(len(v) for v in vectors.values())
        print(f'Building similarity graph using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        metric_func = {
            'euclidean': euclidean_similarity,
            'manhattan': manhattan_similarity,
            'cosine': cosine_similarity,
            'pearson': pearson_similarity
        }[metric]
        sim_graph, sim_mat = similarity_graph(vectors, dims, metric_func, threshold)
        print('The following similarity matrix was produced ...')
        print()
        print('<table>')
        print('<thead><tr>')
        print('<th></th>')
        for l in sorted(sim_mat.leaf_ids_it()):
            print(f'<th>{l}</th>')
        print('</tr></thead>')
        print('<tbody>')
        for l1 in sorted(sim_mat.leaf_ids_it()):
            print('<tr>')
            print(f'<td>{l1}</td>')
            for l2 in sorted(sim_mat.leaf_ids_it()):
                print(f'<td>{sim_mat[l1, l2]:.2f}</td>')
            print('</tr>')
        print('</tbody>')
        print('</table>')
        print()
        print(f'The following similarity graph was produced ...')
        print()
        print('```{dot}')
        print(f'{to_dot(sim_graph)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")













# MARKDOWN_ADJUST
def similarity_to_cluster(
        n: str,
        cluster: set[str],
        sim_mat: SimilarityMatrix
) -> float:
    return mean(sim_mat[n, n_c] for n_c in cluster)


def adjust_cluster(
        sim_graph: Graph,
        sim_mat: SimilarityMatrix,
        cluster: set[str],
        threshold: float
) -> bool:
    # Add closest NOT in cluster
    outside_cluster = set(n for n in sim_graph.get_nodes() if n not in cluster)
    closest = max(
        ((similarity_to_cluster(n, cluster, sim_mat), n) for n in outside_cluster),
        default=None
    )
    add_closest = closest is not None and closest[0] > threshold
    if add_closest:
        cluster.add(closest[1])
    # Remove farthest in cluster
    farthest = min(
        ((similarity_to_cluster(n, cluster, sim_mat), n) for n in cluster),
        default=None
    )
    remove_farthest = farthest is not None and farthest[0] <= threshold
    if remove_farthest:
        cluster.remove(farthest[1])
    # Return true if cluster didn't change (consistent cluster)
    return not add_closest and not remove_farthest
# MARKDOWN_ADJUST


# MARKDOWN_CAST
def cast(
        sim_graph: Graph,
        sim_mat: SimilarityMatrix,
        threshold: float
) -> list[set[str]]:
    # Copy similarity graph because it will get modified by this algorithm
    g = sim_graph.copy()
    # Pull out corrupted cliques and attempt to correct them
    clusters = []
    while len(g) > 0:
        _, start_n = max((g.get_degree(n), n) for n in g.get_nodes())  # highest degree node
        c = {start_n}
        consistent = False
        while not consistent:
            consistent = adjust_cluster(g, sim_mat, c, threshold)
        clusters.append(c)
        for n in c:
            if g.has_node(n):
                g.delete_node(n)
    return clusters
# MARKDOWN_CAST


def clusters_to_similarity_graph(clusters: list[set[str]]) -> Graph:
    sim_graph = Graph()
    for c in clusters:
        for n in c:
            sim_graph.insert_node(n)
        for n1, n2 in combinations(c, r=2):
            e = f'E{sorted([n1, n2])}'
            sim_graph.insert_edge(e, n1, n2)
    return sim_graph


def main_cast():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        vectors = {k: tuple(v) for k, v in data['vectors'].items()}
        metric = data['metric']
        threshold = data['threshold']
        dims = max(len(v) for v in vectors.values())
        print(f'Building similarity graph and executing cluster affinity search technique (CAST) using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        metric_func = {
            'euclidean': euclidean_similarity,
            'manhattan': manhattan_similarity,
            'cosine': cosine_similarity,
            'pearson': pearson_similarity
        }[metric]
        sim_graph, sim_mat = similarity_graph(vectors, dims, metric_func, threshold)
        clusters = cast(sim_graph, sim_mat, threshold)
        sim_graph_fixed = clusters_to_similarity_graph(clusters)
        print('The following similarity matrix was produced ...')
        print()
        print('<table>')
        print('<thead><tr>')
        print('<th></th>')
        for l in sorted(sim_mat.leaf_ids_it()):
            print(f'<th>{l}</th>')
        print('</tr></thead>')
        print('<tbody>')
        for l1 in sorted(sim_mat.leaf_ids_it()):
            print('<tr>')
            print(f'<td>{l1}</td>')
            for l2 in sorted(sim_mat.leaf_ids_it()):
                print(f'<td>{sim_mat[l1, l2]:.2f}</td>')
            print('</tr>')
        print('</tbody>')
        print('</table>')
        print()
        print(f'The following _original_ similarity graph was produced ...')
        print()
        print('```{dot}')
        print(f'{to_dot(sim_graph)}')
        print('```')
        print()
        print(f'The following _corrected_ similarity graph was produced ...')
        print()
        print('```{dot}')
        print(f'{to_dot(sim_graph_fixed)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main_cast()
