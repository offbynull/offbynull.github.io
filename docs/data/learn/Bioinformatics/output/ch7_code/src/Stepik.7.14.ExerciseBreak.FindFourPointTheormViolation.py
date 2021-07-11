import itertools
from itertools import permutations, product, combinations

d = [
    [0, 3, 4, 3],
    [3, 0, 4, 5],
    [4, 4, 0, 2],
    [3, 5, 2, 0]
]
n = len(d)

# This is the obvious way to do it..

# for i, j, k, l in permutations(range(0, n), r=4):
#     s1 = d[i][j] * d[k][l]
#     s2 = d[i][k] + d[j][l]
#     s3 = d[i][l] + d[j][k]
#     if not (s1 <= s2 == s3):
#         print(f'{i, j, k, l}')


# Is there some optimization here that I'm missing? How about this...

# Given nodes 0,1,2,3... the combos you need to try are...
# 0,1
#    2,3
#    3,2 -- same as 2,3
# 0,2
#    1,3
#    3,1 -- same as 1,3
# 0,3
#    1,2
#    2,1 -- same as 1,2
# 1,0 -- same as 0,1
# 1,2
#    3,0
#    0,3 -- same as 3,0
# 1,3
#    2,0
#    0,2 -- same as 2,0
# 2,0 -- same as 0,2
# 2,1 -- same as 1,2
# 2,3
#    0,1
#    1,0 -- same as 0,1
# 3,0 -- same as 0,3
# 3,1 -- same as 1,3
# 3,2 -- same as 2,3

leaf_test_orders = {
    (0, 1, 2, 3),
    (0, 2, 1, 3),
    (0, 3, 1, 2),
    (1, 2, 0, 3),
    (1, 3, 0, 2),
    (2, 3, 0, 1)
}

def four_point_test(i, j, k, l):
    s1 = d[i][j] * d[k][l]
    s2 = d[i][k] + d[j][l]
    s3 = d[i][l] + d[j][k]
    return s1 <= s2 == s3

for leafs in combinations(range(n), r=4):  # this will give back combos of leaf nodes size=4
    passed = False
    for i0, i1, i2, i3 in leaf_test_orders:  # for each set of leaf nodes, test with different orders
        passed = four_point_test(leafs[i0], leafs[i1], leafs[i2], leafs[i3])
        if passed:
            break
    if not passed:
        raise ValueError('Not additive!')