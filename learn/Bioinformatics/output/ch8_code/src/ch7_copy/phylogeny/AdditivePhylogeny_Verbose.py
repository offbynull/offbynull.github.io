from __future__ import annotations

from sys import stdin
from typing import Callable, TypeVar

from ch7_copy.distance_matrix.DistanceMatrix import DistanceMatrix
from graph.UndirectedGraph import Graph
from helpers.InputUtils import str_to_list
from ch7_copy.phylogeny.FourPointCondition import is_additive
from ch7_copy.phylogeny.Trimmer import trim_distance_matrix
from ch7_copy.phylogeny.UntrimTree import create_distance_matrix, untrim_tree


N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')


def to_dot(g: Graph) -> str:
    ret = 'graph G {\n'
    ret += ' graph[rankdir=LR]\n'
    ret += ' node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = sorted(g.get_nodes())
    for n in nodes:
        ret += f'{n}\n'
    for e in sorted(g.get_edges()):
        n1, n2, weight = g.get_edge(e)
        ret += f'{n1} -- {n2} [label="{weight}"]\n'
    ret += '}'
    return ret


def to_html(dm: DistanceMatrix) -> str:
    ret = ''
    ret += '<table>'
    ret += '<thead><tr>'
    ret += '<th></th>'
    for l in sorted(dm.leaf_ids_it()):
        ret += f'<th>{l}</th>'
    ret += '</tr></thead>'
    ret += '<tbody>'
    for l1 in sorted(dm.leaf_ids_it()):
        ret += '<tr>'
        ret += f'<td>{l1}</td>'
        for l2 in sorted(dm.leaf_ids_it()):
            ret += f'<td>{dm[l1, l2]}</td>'
        ret += '</tr>'
    ret += '</tbody>'
    ret += '</table>'
    return ret


# MARKDOWN_OBVIOUS_TREE
def to_obvious_graph(
        dm: DistanceMatrix[N],
        gen_edge_id: Callable[[], N]
) -> Graph:
    if dm.n != 2:
        raise ValueError('Distance matrix must only contain 2 leaf nodes')
    l1, l2 = dm.leaf_ids()
    g = Graph()
    g.insert_node(l1)
    g.insert_node(l2)
    g.insert_edge(
        gen_edge_id(),
        l1,
        l2,
        dm[l1, l2]
    )
    return g
# MARKDOWN_OBVIOUS_TREE


# EXACT SAME AS AdditivePhylogeny BUT SOME CALLBACKS ADDED IN TO MAKE THE OUTPUT MORE VERBOSE
# MARKDOWN
def additive_phylogeny(
        dm: DistanceMatrix[N],
        gen_node_id: Callable[[], N],
        gen_edge_id: Callable[[], E],
        output_dm_callback: Callable[[str, DistanceMatrix], None],
        output_tree_callback: Callable[[str, Graph], None]
) -> Graph:
    if dm.n == 2:
        g = to_obvious_graph(dm, gen_edge_id)
        output_tree_callback('Obvious simple tree...', g)
        return g
    n = next(dm.leaf_ids_it())
    dm_untrimmed = dm.copy()
    trim_distance_matrix(dm, n)
    output_dm_callback(f'Trimmed {n} to produce distance matrix ...', dm)
    g = additive_phylogeny(dm, gen_node_id, gen_edge_id, output_dm_callback, output_tree_callback)
    untrim_tree(dm_untrimmed, g, gen_node_id, gen_edge_id)
    output_tree_callback(f'Attached {n} to produce tree...', g)
    return g
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        # Read matrix
        mat = []
        for line in stdin:
            row = [float(e) for e in str_to_list(line.strip(), 0)[0]]
            mat.append(row)
        dist_mat = create_distance_matrix(mat)
        assert is_additive(dist_mat)
        print('Given the distance matrix ...')
        print()
        print(to_html(dist_mat))
        print()
        _next_edge_id = 0
        def gen_edge_id():
            nonlocal _next_edge_id
            _next_edge_id += 1
            return f'E{_next_edge_id}'
        _next_node_id = 0
        def gen_node_id():
            nonlocal _next_node_id
            _next_node_id += 1
            return f'N{_next_node_id}'
        def output_dm(ctx: str, _dist_mat: DistanceMatrix) :
            print()
            print(ctx)
            print()
            print(to_html(_dist_mat))
            print()
        def output_tree(ctx: str, _tree: Graph):
            print()
            print(ctx)
            print()
            print('```{dot}')
            print(f'{to_dot(_tree)}')
            print('```')
            print()
        tree = additive_phylogeny(dist_mat, gen_node_id, gen_edge_id, output_dm, output_tree)
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
