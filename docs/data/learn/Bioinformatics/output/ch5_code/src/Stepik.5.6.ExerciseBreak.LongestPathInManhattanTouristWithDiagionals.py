# This is very similar to the LongestPathInManhattanTourist code challenge (5.6), but it also features diagonal edges
# in addition to down and right edges.
#
# The DAG to compute is as follows:
#
#      3     2     4     0
#   ?---->?---->?---->?---->?
#  1| \  0| \  2| \  4| \  3|
#   |  \5 |  \0 |  \2 |  \1 |
#   |   \ |   \ |   \ |   \ |
#   v  3 vv  2 vv  4 vv  2 vv
#   ?---->?---->?---->?---->?
#  4| \  6| \  5| \  2| \  1|
#   |  \8 |  \4 |  \3 |  \0 |
#   |   \ |   \ |   \ |   \ |
#   v  0 vv  7 vv  3 vv  4 vv
#   ?---->?---->?---->?---->?
#  4| \  4| \  5| \  2| \  1|
#   |  \10|  \8 |  \9 |  \5 |
#   |   \ |   \ |   \ |   \ |
#   v  3 vv  3 vv  0 vv  2 vv
#   ?---->?---->?---->?---->?
#  5| \  6| \  8| \  5| \  3|
#   |  \5 |  \6 |  \4 |  \7 |
#   |   \ |   \ |   \ |   \ |
#   v  1 vv  3 vv  2 vv  2 vv
#   ?---->?---->?---->?---->?


n, m = 4, 4
down = [
    [1, 0, 2, 1, 3],
    [4, 6, 5, 2, 1],
    [4, 4, 5, 2, 1],
    [5, 6, 8, 5, 3]
]
right = [
    [3, 2, 4, 0],
    [3, 2, 4, 2],
    [0, 7, 3, 4],
    [3, 3, 0, 2],
    [1, 3, 2, 2]
]
down_right_diag = [
    [5, 0, 2, 1],
    [8, 4, 3, 0],
    [10, 8, 9, 5],
    [5, 6, 4, 7]
]

# create
matrix = [[-1] * (m + 1) for i in range(n + 1)]
matrix[0][0] = 0  # set origin cell to 0
# prime first col
for n_ in range(1, n + 1):
    matrix[n_][0] = matrix[n_ - 1][0] + down[n_ - 1][0]
# prime first row
for m_ in range(1, m + 1):
    matrix[0][m_] = matrix[0][m_ - 1] + right[0][m_ - 1]

# compute remainder of grid
for n_ in range(1, n + 1):
    for m_ in range(1, m + 1):
        down_weight = matrix[n_ - 1][m_] + down[n_ - 1][m_]
        right_weight = matrix[n_][m_ - 1] + right[n_][m_ - 1]
        down_right_diag_weight = matrix[n_ - 1][m_ - 1] + down_right_diag[n_ - 1][m_ - 1]
        matrix[n_][m_] = max(down_weight, right_weight, down_right_diag_weight)

# for row in matrix:
#     print(f'{row}')
print(f'{matrix[-1][-1]}')