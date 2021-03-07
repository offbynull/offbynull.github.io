# Exercise Break: How many permutations of length 200 have exactly 199 adjacencies?

# Adjacency is defined as a adjacent pair in the permutation where the 2nd value is 1 ahead of the first: (n, n+1)
# Do tests for smaller dimensions and try to pick out a pattern...

from itertools import permutations, product
from typing import List

from helpers.Utils import slide_window


def count_adj(p: List[int]) -> int:
    return sum(1 if x1 + 1 == x2 else 0 for (x1, x2), _ in slide_window(p, 2))


def count_bp(p: List[int]) -> int:
    return sum(0 if x1 + 1 == x2 else 1 for (x1, x2), _ in slide_window(p, 2))


def test(count: int):
    found = set()
    for n in permutations(range(0, count + 2)):  # instead of 1 to n, the chapter now says to make it 0 to n+1 where 0 and n+1 are implied AND fixed into place
        for signed_n in product(*([n[i], -n[i]] for i in range(len(n)))):
            if signed_n[0] != 0 or signed_n[-1] != count + 1:  # 0 and n+1 must be fixed into place at first and last idx respectively
                continue
            adjs = count_adj(list(signed_n))
            if adjs == count - 1:
                found.add(signed_n)
    print(f'{len(found)} -- {found}')


test(3)  # 6 -- {(0, 1, -3, -2, 4), (0, 1, 2, -3, 4), (0, -2, -1, 3, 4), (0, -3, -2, -1, 4), (0, 1, -2, 3, 4), (0, -1, 2, 3, 4)}
test(4)  # 10 -- {(0, -4, -3, -2, -1, 5), (0, 1, 2, 3, -4, 5), (0, 1, -4, -3, -2, 5), (0, -2, -1, 3, 4, 5), (0, 1, -3, -2, 4, 5), (0, -1, 2, 3, 4, 5), (0, 1, 2, -3, 4, 5), (0, -3, -2, -1, 4, 5), (0, 1, 2, -4, -3, 5), (0, 1, -2, 3, 4, 5)}
test(5)  # 15 -- {(0, 1, 2, 3, 4, -5, 6), (0, 1, 2, -3, 4, 5, 6), (0, -2, -1, 3, 4, 5, 6), (0, 1, -3, -2, 4, 5, 6), (0, 1, 2, 3, -5, -4, 6), (0, 1, 2, -5, -4, -3, 6), (0, -4, -3, -2, -1, 5, 6), (0, 1, 2, 3, -4, 5, 6), (0, -5, -4, -3, -2, -1, 6), (0, 1, -2, 3, 4, 5, 6), (0, -3, -2, -1, 4, 5, 6), (0, 1, 2, -4, -3, 5, 6), (0, -1, 2, 3, 4, 5, 6), (0, 1, -5, -4, -3, -2, 6), (0, 1, -4, -3, -2, 5, 6)}

# The pattern seems to be for n, n+n-1+n-2+...+1 3 it's 3 + 1. So for 100, ...:
print(f'{sum(range(1, 200 + 1))}')  # 20100
