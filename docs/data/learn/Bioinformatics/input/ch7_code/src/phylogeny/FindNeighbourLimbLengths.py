from statistics import mean
from sys import stdin
from typing import TypeVar

from distance_matrix.DistanceMatrix import DistanceMatrix
from helpers.InputUtils import str_to_list

N = TypeVar('N')


# MARKDOWN
def approximate_limb_length_using_neighbour(dm: DistanceMatrix, l: N, l_neighbour: N) -> float:
    leaf_nodes = dm.leaf_ids()
    leaf_nodes.remove(l)
    leaf_nodes.remove(l_neighbour)
    lengths = []
    for k in leaf_nodes:
        length = (dm[l, l_neighbour] + dm[l, k] - dm[l_neighbour, k]) / 2
        lengths.append(length)
    return mean(lengths)


def find_neighbouring_limb_lengths(dm: DistanceMatrix, l1: N, l2: N) -> tuple[float, float]:
    l1_len = approximate_limb_length_using_neighbour(dm, l1, l2)
    l2_len = approximate_limb_length_using_neighbour(dm, l2, l1)
    return l1_len, l2_len
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        mat = []
        leaf1_id = int(stdin.readline().strip())
        leaf2_id = int(stdin.readline().strip())
        for line in stdin:
            row = [float(e) for e in str_to_list(line.strip(), 0)[0]]
            mat.append(row)
        dist_mat = DistanceMatrix.create_from_matrix(mat)
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
