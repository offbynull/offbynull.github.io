from itertools import product
from typing import TypeVar

from ch7_copy.distance_matrix.DistanceMatrix import DistanceMatrix
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
def total_distance(dist_mat: DistanceMatrix[N]) -> dict[N, float]:
    ret = {}
    for l1 in dist_mat.leaf_ids():
        ret[l1] = sum(dist_mat[l1, l2] for l2 in dist_mat.leaf_ids())
    return ret


def neighbour_joining_matrix(dist_mat: DistanceMatrix[N]) -> DistanceMatrix[N]:
    tot_dists = total_distance(dist_mat)
    n = dist_mat.n
    ret = dist_mat.copy()
    for l1, l2 in product(dist_mat.leaf_ids(), repeat=2):
        if l1 == l2:
            continue
        ret[l1, l2] = tot_dists[l1] + tot_dists[l2] - (n - 2) * dist_mat[l1, l2]
    return ret


def find_neighbours(dist_mat: DistanceMatrix[N]) -> tuple[N, N]:
    nj_mat = neighbour_joining_matrix(dist_mat)
    found_pair = None
    found_nj_val = -1
    for l1, l2 in product(nj_mat.leaf_ids_it(), repeat=2):
        if nj_mat[l1, l2] > found_nj_val:
            found_pair = l1, l2
            found_nj_val = nj_mat[l1, l2]
    assert found_pair is not None
    return found_pair
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        dm_raw, _ = str_to_list(input().strip(), 0)
        dm = create_distance_matrix(dm_raw)
        print('Given the following distance matrix...')
        print()
        print('<table>')
        print('<thead><tr>')
        print('<th></th>')
        for l in sorted(dm.leaf_ids()):
            print(f'<th>{l}</th>')
        print('</tr></thead>')
        print('<tbody>')
        for l1 in sorted(dm.leaf_ids()):
            print('<tr>')
            print(f'<td>{l1}</td>')
            for l2 in sorted(dm.leaf_ids()):
                print(f'<td>{dm[l1,l2]}</td>')
            print('</tr>')
        print('</tbody>')
        print('</table>')
        print()
        njm = neighbour_joining_matrix(dm)
        print('... the neighbour joining matrix is ...')
        print()
        print('<table>')
        print('<thead><tr>')
        print('<th></th>')
        for l in sorted(njm.leaf_ids()):
            print(f'<th>{l}</th>')
        print('</tr></thead>')
        print('<tbody>')
        for l1 in sorted(njm.leaf_ids()):
            print('<tr>')
            print(f'<td>{l1}</td>')
            for l2 in sorted(njm.leaf_ids()):
                print(f'<td>{njm[l1,l2]}</td>')
            print('</tr>')
        print('</tbody>')
        print('</table>')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
