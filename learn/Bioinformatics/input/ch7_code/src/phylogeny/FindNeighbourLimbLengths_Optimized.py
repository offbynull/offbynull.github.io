from statistics import mean
from sys import stdin
from typing import TypeVar

from distance_matrix.DistanceMatrix import DistanceMatrix
from helpers.InputUtils import str_to_list

N = TypeVar('N')


def create_distance_matrix(m: list[list[float]]) -> DistanceMatrix:
    d = {}
    for i in range(len(m)):
        for j in range(len(m)):
            i1, i2 = sorted([i, j])
            d[(f'v{i1}', f'v{i2}')] = float(m[i1][i2])
    return DistanceMatrix(d)


# MARKDOWN
def find_neighbouring_limb_lengths(dm: DistanceMatrix[N], l1: N, l2: N) -> tuple[float, float]:
    l1_dist_sum = sum(dm[l1, k] for k in dm.leaf_ids())
    l2_dist_sum = sum(dm[l2, k] for k in dm.leaf_ids())
    res = (l1_dist_sum - l2_dist_sum) / (dm.n - 2)
    l1_len = (dm[l1, l2] + res) / 2
    l2_len = (dm[l1, l2] - res) / 2
    return l1_len, l2_len
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        mat = []
        leaf1_id = stdin.readline().strip()
        leaf2_id = stdin.readline().strip()
        for line in stdin:
            row = [float(e) for e in str_to_list(line.strip(), 0)[0]]
            mat.append(row)
        dist_mat = create_distance_matrix(mat)
        print('Given distance matrix...')
        print()
        print('<table>')
        print('<thead><tr>')
        print('<th></th>')
        for l in sorted(dist_mat.leaf_ids_it()):
            print(f'<th>{l}</th>')
        print('</tr></thead>')
        print('<tbody>')
        for l1 in sorted(dist_mat.leaf_ids_it()):
            print('<tr>')
            print(f'<td>{l1}</td>')
            for l2 in sorted(dist_mat.leaf_ids_it()):
                print(f'<td>{dist_mat[l1, l2]}</td>')
            print('</tr>')
        print('</tbody>')
        print('</table>')
        print()
        print(f'... and given that {leaf1_id} and {leaf2_id} are neighbours, the limb length for leaf node ...')
        leaf1_limb_len, leaf2_limb_len = find_neighbouring_limb_lengths(dist_mat, leaf1_id, leaf2_id)
        print(f' * {leaf1_id} is approximated to be {leaf1_limb_len}')
        print(f' * {leaf2_id} is approximated to be {leaf2_limb_len}')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
