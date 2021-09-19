from itertools import combinations
from sys import stdin
from typing import TypeVar

from distance_matrix.DistanceMatrix import DistanceMatrix
from helpers.InputUtils import str_to_list

N = TypeVar('N')


# MARKDOWN_QUARTET_TEST
def four_point_test(dm: DistanceMatrix, l0: N, l1: N, l2: N, l3: N) -> bool:
    # Pairs of leaf node pairs
    pair_combos = (
        ((l0, l1), (l2, l3)),
        ((l0, l2), (l1, l3)),
        ((l0, l3), (l1, l2))
    )
    # Different orders to test pair_combos to see if they match conditions
    test_orders = (
        (0, 1, 2),
        (0, 2, 1),
        (1, 2, 0)
    )
    # Find at least one order of pair combos that passes the test
    for p1_idx, p2_idx, p3_idx in test_orders:
        p1_1, p1_2 = pair_combos[p1_idx]
        p2_1, p2_2 = pair_combos[p2_idx]
        p3_1, p3_2 = pair_combos[p3_idx]
        s1 = dm[p1_1] + dm[p1_2]
        s2 = dm[p2_1] + dm[p2_2]
        s3 = dm[p3_1] + dm[p3_2]
        if s1 <= s2 == s3:
            return True
    return False
# MARKDOWN_QUARTET_TEST


# MARKDOWN
def is_additive(dm: DistanceMatrix) -> bool:
    # Recall that an additive distance matrix of size <= 3 is guaranteed to be an additive distance
    # matrix (try it and see -- any distances you use will always end up fitting a tree). Thats why
    # you need at least 4 leaf nodes to test.
    if dm.n < 4:
        return True
    leaves = dm.leaf_ids()
    for quartet in combinations(leaves, r=4):
        passed = four_point_test(dm, *quartet)
        if not passed:
            return False
    return True
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        mat = []
        for line in stdin:
            row = [float(e) for e in str_to_list(line.strip(), 0)[0]]
            mat.append(row)
        dist_mat = DistanceMatrix.create_from_matrix(mat)
        print('The distance matrix...')
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
        if is_additive(dist_mat):
            print('... is additive.')
        else:
            print('... is NOT additive.')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
