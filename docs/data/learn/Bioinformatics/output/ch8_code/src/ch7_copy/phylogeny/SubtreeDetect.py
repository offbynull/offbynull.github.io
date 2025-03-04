from sys import stdin
from typing import TypeVar

from ch7_copy.distance_matrix.DistanceMatrix import DistanceMatrix
from helpers.InputUtils import str_to_list
from ch7_copy.phylogeny.FourPointCondition import is_additive
from ch7_copy.phylogeny.FindLimbLength import find_limb_length

N = TypeVar('N')


def create_distance_matrix(m: list[list[float]]) -> DistanceMatrix:
    d = {}
    for i in range(len(m)):
        for j in range(len(m)):
            i1, i2 = sorted([i, j])
            d[(f'v{i1}', f'v{i2}')] = float(m[i1][i2])
    return DistanceMatrix(d)


# MARKDOWN
def is_same_subtree(dm: DistanceMatrix[N], l: N, a: N, b: N) -> bool:
    l_weight = find_limb_length(dm, l)
    test_res = (dm[l, a] + dm[l, b] - dm[a, b]) / 2
    if test_res == l_weight:
        return False
    elif test_res > l_weight:
        return True
    else:
        raise ValueError('???')  # not additive distance matrix?
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        mat = []
        split_leaf_id = stdin.readline().strip()
        test_leaf_id1, test_leaf_id2 = [v for v in stdin.readline().strip().split()]
        for line in stdin:
            row = [float(e) for e in str_to_list(line.strip(), 0)[0]]
            mat.append(row)
        dist_mat = create_distance_matrix(mat)
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
        print(f'Had the tree been split on leaf node {split_leaf_id}\'s parent, leaf nodes {test_leaf_id1} and {test_leaf_id2} would reside in ')
        same_subtree = is_same_subtree(dist_mat, split_leaf_id, test_leaf_id1, test_leaf_id2)
        if same_subtree:
            print('the same subtree.')
        else:
            print('different subtrees.')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
