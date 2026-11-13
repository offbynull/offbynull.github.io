import math
import random
from math import sqrt
from typing import TypeVar

from graph import UndirectedGraph
from helpers.Utils import slide_window

N = TypeVar('N', int, float)


def find_path_in_tree_between_leaves(g: UndirectedGraph.Graph, n: str, end_n: str, n_walk: list[str]):
    n_walk.append(n)
    if n == end_n:
        return True
    for e in g.get_outputs(n):
        n1, n2, _ = g.get_edge(e)
        if len(n_walk) >= 2 and {n1, n2} == {n_walk[-1], n_walk[-2]}:
            continue
        next_n = next(iter({n1, n2}.difference({n})))
        done = find_path_in_tree_between_leaves(g, next_n, end_n, n_walk)
        if done:
            return True
    n_walk.pop()


def sum_path(g: UndirectedGraph.Graph, n_walk: list[str]):
    if len(n_walk) == 1:
        return 0
    ret = 0
    for (n1, n2), _ in slide_window(n_walk, 2):
        for e_id in g.get_outputs(n1):
            e_n1, e_n2, dist = g.get_edge(e_id)
            if {n1, n2} == {e_n1, e_n2}:
                ret += dist
    return ret


def to_distance_matrix(g: UndirectedGraph.Graph) -> list[list[N]]:
    leaf_nodes = sorted([n for n in g.get_nodes() if g.get_degree(n) == 1])
    dist_mat = [[0] * len(leaf_nodes) for _ in leaf_nodes]
    for i, l1 in enumerate(leaf_nodes):
        for j, l2 in enumerate(leaf_nodes):
            path = []
            find_path_in_tree_between_leaves(g, l1, l2, path)
            dist = sum_path(g, path)
            dist_mat[i][j] = dist
    return dist_mat


def sse(real: list[N], predicted: list[N]) -> N:
    res = 0
    for r_val, p_val in zip(real, predicted):
        err = r_val - p_val
        res += err ** 2
    return res


# PROBLEM JUST BEFORE EXERCISE BREAK
# ----------------------------------
# Consider the following labeled tree T and distance matrix D. Compute Discrepancy(T, D).
#
# T =    v1             v3
#          \           /
#         3 \    5    / 1
#            *-------*
#         4 /         \ 2
#          /           \
#        v2             v4
#
#  D =      v1 v2 v3 v4
#        v1  0  4  3  4
#        v2  3  0  4  5
#        v3  4  4  0  2
#        v4  3  5  2  0
#
# Discrepancy(T,D) is the sum of errors squared across leaf pairs WITHOUT duplicates. So for example, if you included
# (v1,v3) in the calculation don't include (v3,v1).
def calculate_sse_part1():
    g = UndirectedGraph.Graph()
    g.insert_node('v1')
    g.insert_node('v2')
    g.insert_node('v3')
    g.insert_node('v4')
    g.insert_node('i0')
    g.insert_node('i1')
    g.insert_edge('e1', 'v1', 'i0', 3)
    g.insert_edge('e2', 'v2', 'i0', 4)
    g.insert_edge('e3', 'i0', 'i1', 5)
    g.insert_edge('e4', 'i1', 'v3', 1)
    g.insert_edge('e5', 'i1', 'v4', 2)
    predicted = to_distance_matrix(g)
    real = [
        [0, 3, 4, 3],
        [3, 0, 4, 5],
        [4, 4, 0, 2],
        [3, 5, 2, 0]
    ]
    # Remember that a distance matrix is mirrored along the diagonal. As such, it contains each distance TWICE (e.g.
    # dist(v1, v3) is the same as dist(v3, v1)). When computing sum of errors squared, DON'T SUBMIT DUPLICATE DISTANCES.
    # So for example, instead of submitting every distance in the real distance matrix, remove everything after the
    # diagonal so that each distance is only represented once (e.g. dist(v1, v3) but no dist(v3, v1))...
    #
    #      v1 v2 v3 v4              v1 v2 v3 v4
    #   v1  0  3  4  3            v1    3  4  3
    #   v2  3  0  4  5    ---->   v2       4  5
    #   v3  4  4  0  2            v3          2
    #   v4  3  5  2  0            v4
    predicted_flattened = [item for i, row in enumerate(predicted) for j, item in enumerate(row[i+1:])]
    real_flattened = [item for i, row in enumerate(real) for j, item in enumerate(row[i+1:])]
    print(f'{sse(real_flattened, predicted_flattened)}')


# EXERCISE BREAK
# --------------
# Exercise Break: Let T be the tree shown below.
#
# T =    v1             v3
#          \           /
#           \         /
#            *-------*
#           /         \
#          /           \
#        v2             v4
#
# Given the non-additive 4 × 4 distance matrix D below, find the lengths of edges in this tree that minimize
# Discrepancy(T, D).  Hint: It isn't the lengths given on the previous step :)
#
#  D =      v1 v2 v3 v4
#        v1  0  4  3  4
#        v2  3  0  4  5
#        v3  4  4  0  2
#        v4  3  5  2  0
#
# Discrepancy(T,D) is the sum of errors squared across leaf pairs WITHOUT duplicates. So for example, if you included
# (v1,v3) in the calculation don't include (v3,v1).
#
#
# MY SOLUTION
# -----------
# I started out with the edge weights given on the prior problem and began widdling them down until I reached the edge
# weights in this function. The sum of errors squared is 2. There's probably some automated way to do something like
# this (e.g. optimization / linear regression / whatever)
def calculate_sse_part2():
    g = UndirectedGraph.Graph()
    g.insert_node('v1')
    g.insert_node('v2')
    g.insert_node('v3')
    g.insert_node('v4')
    g.insert_node('i0')
    g.insert_node('i1')
    g.insert_edge('e1', 'v1', 'i0', 1)
    g.insert_edge('e2', 'v2', 'i0', 2)
    g.insert_edge('e3', 'i0', 'i1', 2)
    g.insert_edge('e4', 'i1', 'v3', 1)
    g.insert_edge('e5', 'i1', 'v4', 1)
    predicted = to_distance_matrix(g)
    real = [
        [0, 3, 4, 3],
        [3, 0, 4, 5],
        [4, 4, 0, 2],
        [3, 5, 2, 0]
    ]
    # Remember that a distance matrix is mirrored along the diagonal. As such, it contains each distance TWICE (e.g.
    # dist(v1, v3) is the same as dist(v3, v1)). When computing sum of errors squared, DON'T SUBMIT DUPLICATE DISTANCES.
    # So for example, instead of submitting every distance in the real distance matrix, remove everything after the
    # diagonal so that each distance is only represented once (e.g. dist(v1, v3) but no dist(v3, v1))...
    #
    #      v1 v2 v3 v4              v1 v2 v3 v4
    #   v1  0  3  4  3            v1    3  4  3
    #   v2  3  0  4  5    ---->   v2       4  5
    #   v3  4  4  0  2            v3          2
    #   v4  3  5  2  0            v4
    predicted_flattened = [item for i, row in enumerate(predicted) for j, item in enumerate(row[i+1:])]
    real_flattened = [item for i, row in enumerate(real) for j, item in enumerate(row[i+1:])]
    print(f'{sse(real_flattened, predicted_flattened)}')


if __name__ == '__main__':
    # FIRST PART OF PROBLEM (just before exercise break)
    calculate_sse_part1()
    # SECOND PART OF THE PROBLEM (exercise break)
    calculate_sse_part2()
