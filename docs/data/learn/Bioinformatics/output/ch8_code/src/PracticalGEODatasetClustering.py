from __future__ import annotations

import lzma
import re
import string
from statistics import stdev
from sys import stdin

import yaml

from clustering.Soft_HierarchialClustering_NeighbourJoining import to_tree
from clustering.Soft_HierarchialClustering_NeighbourJoining_v2 import to_dot, clustering_neighbour_joining, \
    mean_dist_within_edge_range
from metrics.CosineSimilarity import cosine_distance
from metrics.EuclideanDistance import euclidean_distance
from metrics.ManhattanDistance import manhattan_distance
from metrics.PearsonSimilarity import pearson_distance

# with lzma.open('GDS6010.soft_no_replicates_single_control.xz') as f:
#     dataset = f.read().decode('utf8')
#
# dataset = re.search(r'!dataset_table_begin(.*)!dataset_table_end', dataset, flags=re.DOTALL).group(1).strip()
# table = [l.strip().split('\t') for l in dataset.split('\n')]
#
#
# sample_col_names = [
#     'GSM1626001',  # control @ 24hrs, (treat as no infection)
#     'GSM1626004',  # infection @ 6hrs
#     'GSM1626007',  # infection @ 12 hrs
#     'GSM1626010',  # infection @ 24 hrs
# ]
# gene_col_name = 'ID_REF'
#
# table_header = table[0]
# table_gene_col_idx = table_header.index(gene_col_name)
# table_data_sample_idxes = [i for i, c in enumerate(table_header) if c in sample_col_names]
#
# gene_vectors = {r[table_gene_col_idx]: [float(r[i]) for i in table_data_sample_idxes] for r in table[1:]}
# gene_vectors = {''.join(ch for ch in k if ch not in string.punctuation): v for k, v in gene_vectors.items()}
# gene_vectors = {k: v for k, v in gene_vectors.items() if stdev(v) >= 1.4}  # lower than 1.4 returns too many genes for this code to work (python is too slow)
# # gene_vectors = {k: v for k, v in random.sample(gene_vectors.items(), k=200)}
# print(f'{len(gene_vectors)=}')
#
# _next_edge_id = 0
# _next_node_id = 0
# def gen_edge_id():
#     global _next_edge_id
#     _next_edge_id += 1
#     return f'E{_next_edge_id}'
# def gen_node_id():
#     global _next_node_id
#     _next_node_id += 1
#     return f'N{_next_node_id}'
# dm, tree = to_tree(
#     gene_vectors,
#     4,
#     euclidean_distance,
#     gen_node_id,
#     gen_edge_id,
#
# )
# dist_capture = mean_dist_within_edge_range(tree, (0.7, 0.8))
# clusters = clustering_neighbour_joining(tree, dist_capture)
# graphviz = to_dot_hierarch_clust(tree, clusters, edge_scale=3.0)
# print(graphviz)
# for c in clusters:
#     print(f'{len(c)=} -> {c}')
# print(f'CAPTURED NODE = {sum(len(c) for c in clusters)} / CAPTURED CLUSTERS={len(clusters)}')
#
# for i in range(0, 10):
#     span=i*0.1, (i+1)*0.1
#     dist_capture = mean_dist_within_edge_range(tree, span)
#     clusters = clustering_neighbour_joining(tree, dist_capture)
#     print(f'CAPTURE PERCENTAGE RANGE: {dist_capture}, CAPTURED NODES={sum(len(c) for c in clusters)} / CAPTURED CLUSTERS={len(clusters)}')














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














def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = stdin.read()
        data: dict = yaml.safe_load(data_raw)
        filename = data['filename']
        gene_column = data['gene_column']
        sample_columns = data['sample_columns']
        std_dev_limit = data['std_dev_limit']
        metric = data['metric']
        edge_scale = data.get('edge_scale', 1.0)
        dist_capture = data.get('dist_capture')
        dims = len(sample_columns)
        print(f'Executing neighbour joining phylogeny **soft** clustering using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        with lzma.open(filename) as f:
            dataset = f.read().decode('utf8')
        dataset = re.search(r'!dataset_table_begin(.*)!dataset_table_end', dataset, flags=re.DOTALL).group(1).strip()
        table = [l.strip().split('\t') for l in dataset.split('\n')]
        table_header = table[0]
        table_gene_col_idx = table_header.index(gene_column)
        table_data_sample_idxes = [i for i, c in enumerate(table_header) if c in sample_columns]
        gene_vectors = {r[table_gene_col_idx]: [float(r[i]) for i in table_data_sample_idxes] for r in table[1:]}
        gene_vectors = {''.join(ch for ch in k if ch not in string.punctuation): v for k, v in gene_vectors.items()}
        gene_vectors = {k: v for k, v in gene_vectors.items() if stdev(v) >= std_dev_limit}
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
        dist_mat, tree = to_tree(gene_vectors, dims, metric_func, gen_node_id, gen_edge_id)
        # dist_capture = mean_dist_within_edge_range(tree, (0.4, 0.6))
        clusters = clustering_neighbour_joining(tree, dist_capture)
        # print('The following distance matrix was produced ...')
        # print()
        # print('<table>')
        # print('<thead><tr>')
        # print('<th></th>')
        # for l in sorted(dist_mat.leaf_ids_it()):
        #     print(f'<th>{l}</th>')
        # print('</tr></thead>')
        # print('<tbody>')
        # for l1 in sorted(dist_mat.leaf_ids_it()):
        #     print('<tr>')
        #     print(f'<td>{l1}</td>')
        #     for l2 in sorted(dist_mat.leaf_ids_it()):
        #         print(f'<td>{dist_mat[l1, l2]:.2f}</td>')
        #     print('</tr>')
        # print('</tbody>')
        # print('</table>')
        # print()
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