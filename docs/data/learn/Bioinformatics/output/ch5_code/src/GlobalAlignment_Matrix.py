from typing import List, Any, Optional

from WeightLookup import WeightLookup, Constant2DWeightLookup


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


def global_alignment(v: str, w: str, weight_lookup: WeightLookup, buffer: Optional[List[List[Any]]] = None):
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    if buffer is None:
        buffer = []
        for v_idx in range(v_node_count):
            row = []
            for w_idx in range(w_node_count):
                row.append([-1, None])
            buffer.append(row)
    for v_idx in range(v_node_count):
        buffer[v_idx][0][0] = 0
    for w_idx in range(w_node_count):
        buffer[0][w_idx][0] = 0
    for v_idx in range(1, v_node_count):
        for w_idx in range(1, w_node_count):
            buffer[v_idx][w_idx] = max(
                (buffer[v_idx - 1][w_idx][0] + weight_lookup.lookup(v[v_idx - 1], None), '↓'),
                (buffer[v_idx][w_idx - 1][0] + weight_lookup.lookup(None, w[w_idx - 1]), '→'),
                (buffer[v_idx - 1][w_idx - 1][0] + weight_lookup.lookup(v[v_idx - 1], w[w_idx - 1]), '↘'),
                key=lambda x: x[0]
            )
    return buffer


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
def output_lcs(buffer: List[List[Any]], v: str, i: int, j: int):
    if i == 0 or j == 0:
        return ''
    if buffer[i][j][1] == "↓":
        return output_lcs(buffer, v, i - 1, j)
    elif buffer[i][j][1] == "→":
        return output_lcs(buffer, v, i, j - 1)
    else:
        return output_lcs(buffer, v, i - 1, j - 1) + v[i - 1]


def get_score(buffer: List[List[Any]], v: str, w: str):
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    return buffer[v_node_count - 1][w_node_count - 1]


s1 = 'STEAK'
s2 = 'BREAK'
matrix = global_alignment('STEAK', 'BREAK', Constant2DWeightLookup(1, 0, 0))


import sys
sys.setrecursionlimit(2000)
out = output_lcs(matrix, s1, len(s1), len(s2))
print(f'{out}')