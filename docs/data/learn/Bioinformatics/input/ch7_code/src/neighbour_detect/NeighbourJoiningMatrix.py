from itertools import product
from typing import TypeVar

from distance_matric.DistanceMatrix import DistanceMatrix
from helpers.InputUtils import str_to_list


N = TypeVar('N')


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
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        dm_raw, _ = str_to_list(input().strip(), 0)
        dm = DistanceMatrix.create_from_matrix(dm_raw)
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
