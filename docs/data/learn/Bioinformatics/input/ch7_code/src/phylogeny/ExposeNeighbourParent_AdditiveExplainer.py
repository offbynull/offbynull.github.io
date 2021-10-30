from sys import stdin
from typing import TypeVar, Callable

from distance_matrix.DistanceMatrix import DistanceMatrix
from helpers.InputUtils import str_to_list
from phylogeny.Balder import bald_distance_matrix
from phylogeny.FourPointCondition import is_additive

N = TypeVar('N')


def create_distance_matrix(m: list[list[float]]) -> DistanceMatrix:
    d = {}
    for i in range(len(m)):
        for j in range(len(m)):
            i1, i2 = sorted([i, j])
            d[(f'v{i1}', f'v{i2}')] = float(m[i1][i2])
    return DistanceMatrix(d)


# MARKDOWN
def expose_neighbour_parent(
        dm: DistanceMatrix,
        l1: N,
        l2: N,
        gen_node_id: Callable[[], str]
) -> N:
    bald_distance_matrix(dm, l1)
    bald_distance_matrix(dm, l2)
    m_id = gen_node_id()
    m_dists = {x: (dm[l1, x] + dm[l2, x]) / 2 for x in dm.leaf_ids_it()}
    m_dists[m_id] = 0
    dm.insert(m_id, m_dists)
    dm.delete(l1)
    dm.delete(l2)
    return m_id
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
        assert is_additive(dist_mat), "Must be additive"
        print('Given additive distance matrix...')
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
        print(f'... and given that {leaf1_id} and {leaf2_id} are neighbours, balding and merging {leaf1_id} and {leaf2_id} results in ...')
        _next_node_id = 0
        def gen_node_id():
            nonlocal _next_node_id
            _next_node_id += 1
            return f'N{_next_node_id}'
        expose_neighbour_parent(dist_mat, leaf1_id, leaf2_id, gen_node_id)
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
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
