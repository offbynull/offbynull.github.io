from itertools import product

# EXERCISE BREAK
# --------------
# Exercise Break: Before implementing the neighbor-joining algorithm, try applying it to the additive and non-additive
# distance matrices shown below.
#
#    v1 v2 v3 v4           v1 v2 v3 v4
# v1 0  13 21 22        v1 0  3  4  3
# v2 13 0  12 13        v2 3  0  4  5
# v3 21 12 0  13        v3 4  4  0  2
# v4 22 13 13 0         v4 3  5  2  0


def total_distance(distmat: list[list[float]]) -> list[float]:
    return [sum(row) for row in distmat]


def neighbour_joining_matrix(dist_mat: list[list[float]]) -> list[list[float]]:
    tot_dists = total_distance(dist_mat)
    n = len(dist_mat)
    ret = [[0.0] * len(r) for r in dist_mat]
    for i, j in product(range(n), repeat=2):
        if i == j:
            continue
        ret[i][j] = (n - 2) * dist_mat[i][j] - tot_dists[i] - tot_dists[j]
    return ret


nj_mat_for_additive_mat = neighbour_joining_matrix(
    [
        [0 , 13, 21, 22],
        [13, 0 , 12, 13],
        [21, 12, 0 , 13],
        [22, 13, 13, 0 ]
    ]
)
print('\n'.join([f'{r}' for r in nj_mat_for_additive_mat]))
print()

nj_mat_for_non_additive_mat = neighbour_joining_matrix(
    [
        [0, 3, 4, 3],
        [3, 0, 4, 5],
        [4, 4, 0, 2],
        [3, 5, 2, 0]
    ]
)
print('\n'.join([f'{r}' for r in nj_mat_for_non_additive_mat]))
print()

# MY ATTEMPT AT ANSWERING
# -----------------------
# Every leaf's limb connects it to an internal node, so len(internal_nodes) >= len(leaf_nodes)
# Every internal node is connected to 3 other nodes.
#
# If an internal node is connected to 2 leaf nodes, it must have 1 connection to another internal node
# If an internal node is connected to 1 leaf nodes, it must have 2 connection to another internal node
# If an internal node is connected to 0 leaf nodes, it must have 3 connection to another internal node
#
# For 3 leaf nodes, it must be 1 internal node...
#
#       *
#      /
# *---*
#      \
#       *
#
# For 4 leaf nodes, it must be 2 internal nodes...
#
# *       *
#  \     /
#   *---*
#  /     \
# *       *
#
# For 5 leaf nodes, it'd be the same as 4 leaf nodes but 1 new internal node would have to get injected between the
# edge connecting the existing internal nodes, then the 5th leaf node would branch out from that edge...
#
# *           *
#  \         /
#   *---*---*
#  /    |    \
# *     *     *
#
# And that's the crux of it. After 4 nodes, each new leaf is added by injecting a new internal node between an edge
# connecting existing internal nodes. Meaning...
#
#   1. at 4 leaf nodes, the number of internal nodes MUST be 2  (2 less than the number of leaf nodes: 4-2=2)
#   2. for each leaf node added (past 4), the number of internal nodes MUST increase by exactly 1 (e.g. if 4 leaf nodes
#   had 2 internal nodes, 5 leaf nodes will have 3, 6 leaf nodes will have 4, etc..)
#
# As such, the number of internal nodes is guaranteed to be len(leaf_nodes) - 2

# This isn't really a proof but some basic reasoning
