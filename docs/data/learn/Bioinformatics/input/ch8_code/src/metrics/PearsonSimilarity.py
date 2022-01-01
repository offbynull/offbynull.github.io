from math import sqrt
from statistics import mean
from sys import stdin
from typing import Sequence

import yaml


# MARKDOWN
def pearson_similarity(v: Sequence[float], w: Sequence[float], dims: int):
    v_avg = mean(v)
    w_avg = mean(w)
    vec_avg_diffs_dp = sum((v[i] - v_avg) * (w[i] - w_avg) for i in range(dims))
    dist_to_v_avg = sqrt(sum((v[i] - v_avg) ** 2 for i in range(dims)))
    dist_to_w_avg = sqrt(sum((w[i] - w_avg) ** 2 for i in range(dims)))
    return vec_avg_diffs_dp / (dist_to_v_avg * dist_to_w_avg)
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
        d = pearson_similarity(v, w, dims)
        print(f'Their pearson similarity is {d}')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
