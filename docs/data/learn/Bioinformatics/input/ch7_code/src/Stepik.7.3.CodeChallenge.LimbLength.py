import re
from itertools import product

from graph import UndirectedGraph
from helpers.Utils import slide_window

with open('/home/user/Downloads/dataset_240336_11.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

g = UndirectedGraph.Graph()

lines = [s.strip() for s in data.strip().split('\n')]
mat_size = int(lines[0])
leaf_idx = int(lines[1])
dist_mat = [[int(e) for e in row.split()] for row in lines[2:]]

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
