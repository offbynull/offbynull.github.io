from typing import List

with open('/home/user/Downloads/dataset_240303_5(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

import sys
sys.setrecursionlimit(2000)

lines = data.strip().split('\n')
s1 = lines[0].strip()
s2 = lines[1].strip()

# Not using my Graph class -- using the pseudocode directly provided on the site.
# Not using my Graph class -- using the pseudocode directly provided on the site.
# Not using my Graph class -- using the pseudocode directly provided on the site.


#     LCSBackTrack(v, w)
#         for i ← 0 to |v|
#             si, 0 ← 0
#         for j ← 0 to |w|
#             s0, j ← 0
#         for i ← 1 to |v|
#             for j ← 1 to |w|
#                 match ← 0
#                 if vi-1 = wj-1
#                     match ← 1
#                 si, j ← max{si-1, j , si,j-1 , si-1, j-1 + match }
#                 if si,j = si-1,j
#                     Backtracki, j ← "↓"
#                 else if si, j = si, j-1
#                     Backtracki, j ← "→"
#                 else if si, j = si-1, j-1 + match
#                     Backtracki, j ← "↘"
#         return Backtrack

# HEADS UP: |v| maps to len(v)+1 and |w| maps to len(w)+1
def lcs_backtrack(v: str, w: str):
    lcs_matrix = [[-1] * (len(w) + 1) for i in range(len(v) + 1)]
    backtrack_matrix = [[' '] * (len(w) + 1) for i in range(len(v) + 1)]
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
            if lcs_matrix[i][j] == lcs_matrix[i - 1][j]:
                backtrack_matrix[i][j] = '↓'
            elif lcs_matrix[i][j] == lcs_matrix[i][j - 1]:
                backtrack_matrix[i][j] = '→'
            elif lcs_matrix[i][j] == lcs_matrix[i - 1][j - 1] + match:
                backtrack_matrix[i][j] = '↘'
    return backtrack_matrix


#     OutputLCS(backtrack, v, i, j)
#         if i = 0 or j = 0
#             return ""
#         if backtracki, j = "↓"
#             return OutputLCS(backtrack, v, i - 1, j)
#         else if backtracki, j = "→"
#             return OutputLCS(backtrack, v, i, j - 1)
#         else
#             return OutputLCS(backtrack, v, i - 1, j - 1) + vi

# HEADS UP: vi should actually be vi-1
def output_lcs(backtrack_matrix: List[List[str]], v: str, i: int, j: int):
    if i == 0 or j == 0:
        return ''
    if backtrack_matrix[i][j] == "↓":
        return output_lcs(backtrack_matrix, v, i - 1, j)
    elif backtrack_matrix[i][j] == "→":
        return output_lcs(backtrack_matrix, v, i, j - 1)
    else:
        return output_lcs(backtrack_matrix, v, i - 1, j - 1) + v[i - 1]


backtrack_matrix = lcs_backtrack(s1, s2)
lcs = output_lcs(backtrack_matrix, s1, len(s1), len(s2))
print(f'{lcs}')