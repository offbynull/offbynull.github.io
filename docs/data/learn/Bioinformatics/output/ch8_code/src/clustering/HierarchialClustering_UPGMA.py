from itertools import product
from sys import stdin
from typing import Callable

import yaml

from ch7_copy.distance_matrix.DistanceMatrix import DistanceMatrix
from ch7_copy.phylogeny.UPGMA import upgma
from graph.DirectedGraph import Graph
from metrics.CosineSimilarity import cosine_distance
from metrics.EuclideanDistance import euclidean_distance
from metrics.ManhattanDistance import manhattan_distance
from metrics.PearsonSimilarity import pearson_distance


def to_dot(g: Graph) -> str:
    ret = 'graph G {\n'
    ret += ' graph[rankdir=BT]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = sorted(g.get_nodes())
    for n in nodes:
        weight = g.get_node_data(n)
        ret += f'{n} [label="{n}\\n{weight:.2f}"]\n'
    for e in sorted(g.get_edges()):
        n1, n2, weight = g.get_edge(e)
        ret += f'{n1} -- {n2} [label="{weight:.2f}"]\n'
    ret += '}'
    return ret















DistanceMetric = Callable[[tuple[float], tuple[float], int], float]


# MARKDOWN
def hierarchial_clustering_upgma(
        vectors: dict[str, tuple[float]],
        dims: int,
        distance_metric: DistanceMetric
) -> tuple[DistanceMatrix, Graph]:
    # Generate a distance matrix from the vectors
    dists = {}
    for (k1, v1), (k2, v2) in product(vectors.items(), repeat=2):
        if k1 == k2:
            continue  # skip -- will default to 0
        dists[k1, k2] = distance_metric(v1, v2, dims)
    dist_mat = DistanceMatrix(dists)
    # Run UPGMA on the distance matrix
    tree, _ = upgma(dist_mat.copy())
    # Return
    return dist_mat, tree
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
        print(f'Executing UPGMA clustering using the following settings...')
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
        dist_mat, tree = hierarchial_clustering_upgma(vectors, dims, metric_func)
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
        print(f'The following UPGMA generated tree was produced ...')
        print()
        print('```{dot}')
        print(f'{to_dot(tree)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()