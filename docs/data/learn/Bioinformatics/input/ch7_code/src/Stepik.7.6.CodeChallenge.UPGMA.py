import re
from itertools import product

from graph import UndirectedGraph
from helpers.Utils import slide_window

with open('/home/user/Downloads/test.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = [s.strip() for s in data.strip().split('\n')]
mat_size = int(lines[0])
dist_mat = [[int(e) for e in row.split()] for row in lines[1:]]


def cluster_dist(dist_mat: list[list[float]], cluster1: set[int], cluster2: set[int]) -> float:
    numerator = sum(dist_mat[i][j] for i, j in zip(cluster1, cluster2))
    denominator = len(cluster1) * len(cluster2)
    return numerator / denominator


class NodeData:
    def __init__(self):
        self.age = 0


def upgma(dist_mat: list[list[float]], n: int):
    g = UndirectedGraph.Graph()
    clusters = {i: {i} for i in range(n)}
    for node in range(n):
        nd = NodeData()
        g.insert_node(node, nd)
    while len(clusters) > 1:
        min_n1 = None
        min_n2 = None
        min_dist = None
        for n1, n2 in product(enumerate(clusters.keys()), repeat=2):
            if n1 == n2:
                continue
            d = cluster_dist(dist_mat, clusters[n1], clusters[n2])
            if min_dist is None or d < min_dist:
                min_n1 = n1
                min_n2 = n2
                min_dist = d
        assert min_dist is not None
        n += 1
        new_node = n
        new_nodedata = NodeData()
        new_nodedata.age = min_dist / 2
        g.insert_node(new_node, new_nodedata)
        clusters[new_node] = clusters[min_n1] | clusters[min_n2]
        del clusters[min_n1]
        del clusters[min_n2]

        CONTINUE WORKING ON ME
        CONTINUE WORKING ON ME
        CONTINUE WORKING ON ME
        CONTINUE WORKING ON ME
        CONTINUE WORKING ON ME
        CONTINUE WORKING ON ME
        CONTINUE WORKING ON ME
        CONTINUE WORKING ON ME
        CONTINUE WORKING ON ME
        CONTINUE WORKING ON ME
        CONTINUE WORKING ON ME
        CONTINUE WORKING ON ME
        CONTINUE WORKING ON ME
        CONTINUE WORKING ON ME




min_limb_len = None
for i, k in product(range(mat_size), range(mat_size)):
    if i == leaf_idx or k == leaf_idx:
        continue
    limb_len = (dist_mat[i][leaf_idx] + dist_mat[k][leaf_idx] - dist_mat[i][k]) / 2
    if min_limb_len is None or limb_len < min_limb_len:
        min_limb_len = limb_len
print(f'{int(min_limb_len)}')

# THIS IS GIVING BACK GOOD RESULTS WITH THE TEST DATASETS BUT I DON'T KNOW WHY...
#
# target = sorted(enumerate(dist_mat[leaf_idx]), key=lambda x: x[1])
# target.remove((leaf_idx, 0))
# for ((i1, v1), (i2, v2)), _ in slide_window(target, k=2):
#     limb_len = (dist_mat[i1][leaf_idx] + dist_mat[i2][leaf_idx] - dist_mat[i1][i2]) / 2
#     if min_limb_len is None or limb_len < min_limb_len:
#         min_limb_len = limb_len
#     elif limb_len > min_limb_len:
#         break
# print(f'{int(min_limb_len)}')
