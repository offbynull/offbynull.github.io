from itertools import product
from typing import TypeVar, Any

from ch7_copy.distance_matrix.DistanceMatrix import DistanceMatrix
from graph.UndirectedGraph import Graph
from helpers.InputUtils import str_to_list
from ch7_copy.phylogeny.TreeToSimpleTree import is_tree

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')


def create_graph(edges: list[list[Any]]) -> Graph[str, None, str, float]:
    g = Graph()
    for n in {n for e in edges for n in e[:2]}:
        g.insert_node(n)
    for n1, n2, weight in edges:
        g.insert_edge(f'{n1}-{n2}', n1, n2, float(weight))
    return g


def to_dot(g: Graph) -> str:
    ret = 'graph G {\n'
    ret += ' graph[rankdir=LR]\n'
    ret += ' node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = sorted(g.get_nodes())
    for n in nodes:
        ret += f'{n}\n'
    for e in g.get_edges():
        n1, n2, weight = g.get_edge(e)
        ret += f'{n1} -- {n2} [label="{weight}"]\n'
    ret += '}'
    return ret


# MARKDOWN
def find_path(g: Graph[N, ND, E, float], n1: N, n2: N) -> list[E]:
    if not g.has_node(n1) or not g.has_node(n2):
        ValueError('Node missing')
    if n1 == n2:
        return []
    queued_edges = list()
    for e in g.get_outputs(n1):
        queued_edges.append((n1, [e]))
    while len(queued_edges) > 0:
        ignore_n, e_list = queued_edges.pop()
        e_last = e_list[-1]
        active_n = [n for n in g.get_edge_ends(e_last) if n != ignore_n][0]
        if active_n == n2:
            return e_list
        children = set(g.get_outputs(active_n))
        children.remove(e_last)
        for child_e in children:
            child_ignore_n = active_n
            new_e_list = e_list[:] + [child_e]
            queued_edges.append((child_ignore_n, new_e_list))
    raise ValueError(f'No path from {n1} to {n2}')


def to_additive_distance_matrix(g: Graph[N, ND, E, float]) -> DistanceMatrix[N]:
    leaves = {n for n in g.get_nodes() if g.get_degree(n) == 1}
    dists = {}
    for l1, l2 in product(leaves, repeat=2):
        d = sum(g.get_edge_data(e) for e in find_path(g, l1, l2))
        dists[l1, l2] = d
    return DistanceMatrix(dists)
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
        dist_mat = to_additive_distance_matrix(g)
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