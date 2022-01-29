from typing import TypeVar

from ch7_copy.distance_matrix.DistanceMatrix import DistanceMatrix
from graph.UndirectedGraph import Graph
from helpers.InputUtils import str_to_list
from ch7_copy.phylogeny.TreeToAdditiveDistanceMatrix import create_graph, to_dot, to_additive_distance_matrix
from ch7_copy.phylogeny.TreeToSimpleTree import is_tree, is_simple_tree

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')


# MARKDOWN
def cardinality_test(g: Graph[N, ND, E, float]) -> tuple[DistanceMatrix[N], bool]:
    return (
        to_additive_distance_matrix(g),
        is_simple_tree(g)
    )
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        edges, _ = str_to_list(input().strip(), 0)
        g = create_graph(edges)
        assert is_tree(g)  # Ensure graph is a tree
        print('The tree...')
        print()
        print('```{dot}')
        print(f'{to_dot(g)}')
        print('```')
        print()
        print('... produces the additive distance matrix ...')
        print()
        dist_mat, simple = cardinality_test(g)
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
        if simple:
            print('The tree is simple. This is the ONLY simple tree possible for this additive distance matrix and vice-versa.')
        else:
            print('The tree is NON-simple. This is one of MANY non-simple trees possible for this additive distance matrix.')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()