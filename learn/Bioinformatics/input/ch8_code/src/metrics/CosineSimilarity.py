from math import sqrt
from sys import stdin
from typing import Sequence

import yaml


# MARKDOWN
def cosine_similarity(v: Sequence[float], w: Sequence[float], dims: int):
    vec_dp = sum(v[i] * w[i] for i in range(dims))
    v_mag = sqrt(sum(v[i] ** 2 for i in range(dims)))
    w_mag = sqrt(sum(w[i] ** 2 for i in range(dims)))
    return vec_dp / (v_mag * w_mag)


def cosine_distance(v: Sequence[float], w: Sequence[float], dims: int):
    # To turn cosine similarity into a distance metric, subtract 1.0 from it. By
    # subtracting 1.0, you're changing the bounds from [1.0, -1.0] to [0.0, 2.0].
    #
    # Recall that any distance metric must return 0 when the items being compared
    # are the same and increases the more different they get. By subtracting 1.0,
    # you're matching that distance metric requirement: 0.0 when totally similar
    # and 2.0 for totally dissimilar.
    return 1.0 - cosine_similarity(v, w, dims)
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
        d = cosine_similarity(v, w, dims)
        print(f'Their cosine similarity is {d}')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()

