from math import sqrt
from sys import stdin
from typing import Sequence

import yaml


# MARKDOWN
def manhattan_distance(v: Sequence[float], w: Sequence[float], dims: int):
    x = 0.0
    for i in range(dims):
        x += abs(w[i] - v[i])
    return x


# Unsure if this is a good idea, but it I guess it technically meets the definition
# of a similarity metric: the more similar something is, the "greater" the value it
# produces. But, in this case the maximum similarity is 0. Anything less similar is
# negative ("lesser" than 0).
def manhattan_similarity(v: Sequence[float], w: Sequence[float], dims: int):
    return -manhattan_distance(v, w, dims)
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data = yaml.safe_load(stdin)
        v = data[0]
        w = data[1]
        dims = max(len(v), len(w))
        print('Given the vectors ...')
        print()
        print(f' * {v}')
        print(f' * {w}')
        print()
        d = manhattan_distance(v, w, dims)
        print(f'Their manhattan distance is {d}')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()

