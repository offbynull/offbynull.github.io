from copy import deepcopy
from typing import List


# Revised Stepik.5.8.CodeChallenge.OutputLongestCommonSubsequenceUsingBacktrack to return ALL possible longest common
# subsequences! This explodes out the backtrack matrix on each step, so things get real intensive real fast. It might
# be good to keep track of backtrack_matrixes as a set to avoid duplicates (see helpers/HashableCollections to help with
# this).
#
# If you were using an actual DAG, I think the appropriate thing to do would be to fork out a new path in the DAG for
# each deviation rather than copying the matrix (exploding it) for each deviation.
def lcs_backtrack(v: str, w: str):
    lcs_matrix = [[-1] * (len(w) + 1) for i in range(len(v) + 1)]
    backtrack_matrix_init = [[' '] * (len(w) + 1) for i in range(len(v) + 1)]
    backtrack_matrixes = [backtrack_matrix_init]
    for i in range(len(v)):
        lcs_matrix[i][0] = 0
    for j in range(len(w)):
        lcs_matrix[0][j] = 0
    for i in range(1, len(v) + 1):
        for j in range(1, len(w) + 1):
            match = 0
            if v[i - 1] == w[j - 1]:
                match = 1
            lcs_matrix[i][j] = max(lcs_matrix[i - 1][j], lcs_matrix[i][j - 1], lcs_matrix[i - 1][j - 1] + match)
            new_backtrack_matrixes = []
            for backtrack_matrix in backtrack_matrixes:
                if lcs_matrix[i][j] == lcs_matrix[i - 1][j]:
                    new_backtrack_matrix = deepcopy(backtrack_matrix)
                    new_backtrack_matrix[i][j] = '↓'
                    new_backtrack_matrixes += [new_backtrack_matrix]
                if lcs_matrix[i][j] == lcs_matrix[i][j - 1]:
                    new_backtrack_matrix = deepcopy(backtrack_matrix)
                    new_backtrack_matrix[i][j] = '→'
                    new_backtrack_matrixes += [new_backtrack_matrix]
                if lcs_matrix[i][j] == lcs_matrix[i - 1][j - 1] + match and match == 1:  # Only shove in if its a match
                    new_backtrack_matrix = deepcopy(backtrack_matrix)
                    new_backtrack_matrix[i][j] = '↘'
                    new_backtrack_matrixes += [new_backtrack_matrix]
            backtrack_matrixes = new_backtrack_matrixes
    return backtrack_matrixes


def output_lcs(backtrack_matrix: List[List[str]], v: str, i: int, j: int):
    if i == 0 or j == 0:
        return ''
    if backtrack_matrix[i][j] == "↓":
        return output_lcs(backtrack_matrix, v, i - 1, j)
    elif backtrack_matrix[i][j] == "→":
        return output_lcs(backtrack_matrix, v, i, j - 1)
    else:
        return output_lcs(backtrack_matrix, v, i - 1, j - 1) + v[i - 1]


import sys
sys.setrecursionlimit(2000)

s1 = 'CTGAG'
s2 = 'TGCT'

all_backtrack_matrixes = lcs_backtrack(s1, s2)
lcses = set()
for bm in all_backtrack_matrixes:
    lcs = output_lcs(bm, s1, len(s1), len(s2))
    lcses.add(lcs)

print(f'{lcses}')