from itertools import combinations
from sys import stdin
from typing import TypeVar

from distance_matrix.DistanceMatrix import DistanceMatrix
from helpers.InputUtils import str_to_list
from phylogeny.FourPointCondition import is_additive

N = TypeVar('N')


# MARKDOWN
def find_limb_length(dm: DistanceMatrix, l: N) -> float:
    leaf_nodes = dm.leaf_ids()
    leaf_nodes.remove(l)
    a = leaf_nodes.pop()
    b = min(leaf_nodes, key=lambda x: (dm[l, a] + dm[l, x] - dm[a, x]) / 2)
    return (dm[l, a] + dm[l, b] - dm[a, b]) / 2
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
        leaf_limb_len = find_limb_length(dist_mat, leaf_id)
        print(f'The limb for leaf node {leaf_id} in its unique simple tree has a weight of {leaf_limb_len}')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
