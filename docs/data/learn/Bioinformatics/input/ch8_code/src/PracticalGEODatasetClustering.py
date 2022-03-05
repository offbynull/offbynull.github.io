from __future__ import annotations

import lzma
import random
import re
import string
from collections import defaultdict
from itertools import product
from math import sqrt
from statistics import stdev

from ch7_copy.phylogeny.TreeToAdditiveDistanceMatrix import find_path
from clustering.SimilarityGraph_CAST import similarity_graph, to_dot, cast, clusters_to_similarity_graph
from clustering.Soft_HierarchialClustering_NeighbourJoining import soft_hierarchial_clustering_neighbour_joining, \
    to_dot as to_dot_hierarch_clust, get_leaf_distances
from graph.UndirectedGraph import Graph
from metrics.EuclideanDistance import euclidean_similarity, euclidean_distance
from metrics.PearsonSimilarity import pearson_distance

with lzma.open('GDS6010.soft_no_replicates_single_control.xz') as f:
    dataset = f.read().decode('utf8')

dataset = re.search(r'!dataset_table_begin(.*)!dataset_table_end', dataset, flags=re.DOTALL).group(1).strip()
table = [l.strip().split('\t') for l in dataset.split('\n')]


sample_col_names = [
    'GSM1626001',  # control @ 24hrs, (treat as no infection)
    'GSM1626004',  # infection @ 6hrs
    'GSM1626007',  # infection @ 12 hrs
    'GSM1626010',  # infection @ 24 hrs
]
gene_col_name = 'ID_REF'

table_header = table[0]
table_gene_col_idx = table_header.index(gene_col_name)
table_data_sample_idxes = [i for i, c in enumerate(table_header) if c in sample_col_names]

gene_vectors = {r[table_gene_col_idx]: [float(r[i]) for i in table_data_sample_idxes] for r in table[1:]}
gene_vectors = {''.join(ch for ch in k if ch not in string.punctuation): v for k, v in gene_vectors.items()}
gene_vectors = {k: v for k, v in gene_vectors.items() if stdev(v) >= 1.6}  # lower than 1.4 returns too many genes for this code to work (python is too slow)
# gene_vectors = {k: v for k, v in random.sample(gene_vectors.items(), k=200)}
print(f'{len(gene_vectors)=}')

_next_edge_id = 0
_next_node_id = 0
def gen_edge_id():
    global _next_edge_id
    _next_edge_id += 1
    return f'E{_next_edge_id}'
def gen_node_id():
    global _next_node_id
    _next_node_id += 1
    return f'N{_next_node_id}'
dm, g, _ = soft_hierarchial_clustering_neighbour_joining(
    gene_vectors,
    4,
    euclidean_distance,
    gen_node_id,
    gen_edge_id
)
graphviz = to_dot_hierarch_clust(g, edge_scale=3.0)
print(graphviz)


# similar to SQUARED ERROR DISTORTION -- larger edges have less influence on the avg
def distorted_edge_weight_avg(exp: float):
    edge_count = sum(1 for e in g.get_edges())
    return (sum(g.get_edge_data(e) ** (1/exp) for e in g.get_edges()) / edge_count) ** exp

print(f'{distorted_edge_weight_avg(2)=}')
print(f'{distorted_edge_weight_avg(3)=}')
print(f'{distorted_edge_weight_avg(4)=}')


def find_reachable_leaves(n: str, max_dist: float, total_dist: float = 0.0, from_edge: str | None = None) -> dict[str, list[str]]:
    edges = set(g.get_outputs(n))
    if len(edges) == 1:  # is leaf node?
        return {n: []}
    all_found = {}
    for e in edges:
        if e == from_edge:
            continue
        other_n = g.get_edge_end(e, n)
        dist = g.get_edge_data(e)
        new_total_dist = total_dist + dist
        if new_total_dist > max_dist:
            continue
        found = find_reachable_leaves(other_n, max_dist, new_total_dist, e)
        for e_list in found.values():
            e_list.append(e)
        all_found.update(found)
    return all_found


max_dist = distorted_edge_weight_avg(2) * 5  # anything within ~5 hops
internal_nodes = {n for n in g.get_nodes() if g.get_degree(n) > 1}
leaf_nodes = {n for n in g.get_nodes() if g.get_degree(n) == 1}

leaf_to_edge_list = {}
for n in internal_nodes:
    found = find_reachable_leaves(n, max_dist)
    for n_leaf, edge_list in found.items():
        old_edge_list = leaf_to_edge_list.get(n_leaf)
        if old_edge_list is None or len(edge_list) > len(old_edge_list):
            leaf_to_edge_list[n_leaf] = edge_list

leaf_to_node_list = {}
for n_leaf, edge_list in leaf_to_edge_list.items():
    node_list = [n_leaf]
    for e in edge_list:
        n_next = g.get_edge_end(e, node_list[-1])
        node_list.append(n_next)
    leaf_to_node_list[n_leaf] = node_list


print(f'{leaf_to_node_list}')

internal_node_cluster = defaultdict(set)
for n_leaf, n_list in leaf_to_node_list.items():
    n_internal = n_list[-1]
    internal_node_cluster[n_internal].add(n_leaf)


internal_node_cluster = {k: v for k, v in internal_node_cluster.items() if len(v) > 1}


for n_internal, n_leaves in internal_node_cluster.items():
    print(f'{n_internal=} {n_leaves=}')






















def likelihood_of_ownership(
        tree: Graph[str, None, str, float],
        n: str,
) -> dict[str, tuple[float, float]]:
    # Get dists between n and each to leaf node
    dists = {}
    get_leaf_distances(tree, n, None, 0.0, dists)
    max_dist = max(dists.values())
    return {leaf: (d, 1.0 - (d / max_dist)) for leaf, d in dists.items()}


def dist_between(
        tree: Graph[str, None, str, float],
        from_n: str,
        to_n: str
):
    path = find_path(tree, from_n, to_n)
    return sum(g.get_edge_data(e) for e in path)


ownership = {}
for n in internal_nodes:
    leaf_likelihoods = likelihood_of_ownership(g, n)
    leaf_likelihoods = {n_leaf: (dist, prob) for n_leaf, (dist, prob) in leaf_likelihoods if prob >= 0.8}
    ownership[n] = leaf_likelihoods

owner_dists = {}
for n1, n2 in product(ownership, repeat=2):
    if n1 == n2:
        continue
    d = dist_between(g, n1, n2)
    owner_dists[n1, n2] = d
    owner_dists[n2, n1] = d
ownership = {n: p for n, p in ownership.items() if len(p) > 0}
print(f'{ownership}')


AVERAGE DISTANCES TO LEAVES FOR CLUSTER1
AVERAGE DISTANCES TO LEAVES FOR CLUSTER2
IF DIST(CENTER1, CENTER2) IS <= AVG FOR CLUSTER1 OR AVG FOR CLUSTER2, COMBINE THE CLUSTERS



















# threshold = -1.0
# g, sm = similarity_graph(gene_vectors, len(sample_col_names), euclidean_similarity, threshold)
# clusters = cast(g, sm, threshold)
# g = clusters_to_similarity_graph(clusters)
# graphviz = to_dot(g)
#
# print(graphviz)
# for c in clusters:
#     if len(c) == 1:
#         continue
#     print('--------------')
#     for v in c:
#         print(f'{v} = {gene_vectors[v]}')