import itertools
from itertools import permutations, product, combinations

d = [
    [0, 3, 4, 3],
    [3, 0, 4, 5],
    [4, 4, 0, 2],
    [3, 5, 2, 0]
]
n = len(d)

for i, j, k, l in permutations(range(0, n), r=4):
    s1 = d[i][j] * d[k][l]
    s2 = d[i][k] + d[j][l]
    s3 = d[i][l] + d[j][k]
    if not (s1 <= s2 == s3):
        print(f'{i, j, k, l}')


# Is there some optimization here that I'm missing?
