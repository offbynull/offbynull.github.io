from itertools import combinations
from sys import stdin
from typing import TypeVar

from distance_matrix.DistanceMatrix import DistanceMatrix
from helpers.InputUtils import str_to_list
from phylogeny.FourPointCondition import is_additive
from phylogeny.LimbLength import limb_length

N = TypeVar('N')


# MARKDOWN
def bald(dm: DistanceMatrix, l: N) -> None:
    l_len = limb_length(dm, l)
    for n in dm.leaf_ids_it():
        if n == l:
            continue
        dm[l, n] -= l_len
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        mat = []
        leaf_id = int(stdin.readline().strip())
        for line in stdin:
            row = [float(e) for e in str_to_list(line.strip(), 0)[0]]
            mat.append(row)
        dist_mat = DistanceMatrix.create_from_matrix(mat)
        assert is_additive(dist_mat), 'Not a additive distance matrix'
        print('Given the additive distance matrix...')
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
        print(f'... trimming leaf node {leaf_id} results in ...')
        print()
        bald(dist_mat, leaf_id)
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
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
