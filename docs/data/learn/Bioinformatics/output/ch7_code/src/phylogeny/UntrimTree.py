from itertools import product
from sys import stdin
from typing import TypeVar, Any, Union, Literal, Callable

from distance_matrix.DistanceMatrix import DistanceMatrix
from graph.UndirectedGraph import Graph
from helpers.InputUtils import str_to_list
from phylogeny.Balder import bald_distance_matrix
from phylogeny.FourPointCondition import is_additive
from phylogeny.LimbLength import find_limb_length
from phylogeny.SubtreeDetect import is_same_subtree
from phylogeny.TreeToAdditiveDistanceMatrix import find_path
from phylogeny.TreeToSimpleTree import is_tree

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


def create_distance_matrix(m: list[list[float]]) -> DistanceMatrix:
    d = {}
    for i in range(len(m)):
        for j in range(len(m)):
            i1, i2 = sorted([i, j])
            d[(f'v{i1}', f'v{i2}')] = float(m[i1][i2])
    return DistanceMatrix(d)


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
def find_trimmed_leaf(dist_mat: DistanceMatrix[N], trimmed_tree: Graph[N, ND, E, float]) -> N:
    trimmed_tree_leaves = {n for n in trimmed_tree.get_nodes() if trimmed_tree.get_degree(n) == 1}
    dist_mat_leaves = dist_mat.leaf_ids()
    if len(dist_mat_leaves) - 1 != len(trimmed_tree_leaves):
        raise ValueError(f'Bad inputs {dist_mat_leaves} vs {trimmed_tree_leaves}')
    leaves_diff = dist_mat_leaves - trimmed_tree_leaves
    if len(leaves_diff) != 1:
        raise ValueError(f'Bad inputs {leaves_diff}')
    return leaves_diff.pop()


def find_pair_traveling_thru_leaf_parent(dist_mat: DistanceMatrix, leaf_node: N) -> tuple[N, N]:
    leaf_set = dist_mat.leaf_ids() - {leaf_node}
    for l1, l2 in product(leaf_set, repeat=2):
        if not is_same_subtree(dist_mat, leaf_node, l1, l2):
            return l1, l2
    raise ValueError('Not found')


def find_distance_to_leaf_parent(dist_mat: DistanceMatrix, from_leaf_node: N, to_leaf_node: N) -> float:
    balded_dist_mat = dist_mat.copy()
    bald_distance_matrix(balded_dist_mat, to_leaf_node)
    return balded_dist_mat[from_leaf_node, to_leaf_node]


def walk_until_distance(
        tree: Graph[N, ND, E, float],
        n_start: N,
        n_end: N,
        desired_dist: float
) -> Union[
    tuple[Literal['NODE'], N],
    tuple[Literal['EDGE'], E, N, N, float, float]
]:
    path = find_path(tree, n_start, n_end)
    last_edge_end = n_start
    dist_walked = 0.0
    for edge in path:
        ends = tree.get_edge_ends(edge)
        n1 = last_edge_end
        n2 = next(n for n in ends if n != last_edge_end)
        weight = tree.get_edge_data(edge)
        dist_walked_with_weight = dist_walked + weight
        if dist_walked_with_weight > desired_dist:
            return 'EDGE', edge, n1, n2, dist_walked, weight
        elif dist_walked_with_weight == desired_dist:
            return 'NODE', n2
        dist_walked = dist_walked_with_weight
        last_edge_end = n2
    raise ValueError('Bad inputs')


def untrim_tree(
        dist_mat: DistanceMatrix,
        trimmed_tree: Graph[N, ND, E, float],
        node_id_generator: Callable[[], N],
        edge_id_generator: Callable[[], E]
) -> None:
    trimmed_n = find_trimmed_leaf(dist_mat, trimmed_tree)
    trimmed_limb_len = find_limb_length(dist_mat, trimmed_n)
    leaf1, leaf2 = find_pair_traveling_thru_leaf_parent(dist_mat, trimmed_n)
    trimmed_parent_dist = find_distance_to_leaf_parent(dist_mat, leaf1, trimmed_n)
    res = walk_until_distance(trimmed_tree, leaf1, leaf2, trimmed_parent_dist)
    stopped_on = res[0]
    if stopped_on == 'NODE':
        parent_n = res[1]
    elif stopped_on == 'EDGE':
        edge, n1, n2, walked_dist, edge_weight = res[1:]
        parent_n = node_id_generator()
        trimmed_tree.insert_node(parent_n)
        n1_to_parent_id = edge_id_generator()
        n1_to_parent_weight = trimmed_parent_dist - walked_dist
        trimmed_tree.insert_edge(n1_to_parent_id, n1, parent_n, n1_to_parent_weight)
        parent_to_n2_id = edge_id_generator()
        parent_to_n2_weight = edge_weight - n1_to_parent_weight
        trimmed_tree.insert_edge(parent_to_n2_id, parent_n, n2, parent_to_n2_weight)
        trimmed_tree.delete_edge(edge)
    else:
        raise ValueError('???')
    limb_e = edge_id_generator()
    trimmed_tree.insert_node(trimmed_n)
    trimmed_tree.insert_edge(limb_e, parent_n, trimmed_n, trimmed_limb_len)
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        # Read tree
        edges, _ = str_to_list(stdin.readline().strip(), 0)
        trimmed_tree = create_graph(edges)
        assert is_tree(trimmed_tree)  # Ensure a tree
        # Read matrix
        mat = []
        for line in stdin:
            row = [float(e) for e in str_to_list(line.strip(), 0)[0]]
            mat.append(row)
        dist_mat = create_distance_matrix(mat)
        is_additive(dist_mat)  # Ensure additive
        trimmed_n = find_trimmed_leaf(dist_mat, trimmed_tree)  # Ensure tree is for dist_mat minus a missing limb
        print('Given the distance matrix representing simple tree T...')
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
        print(f'... and simple tree representing trim(T, {trimmed_n})...')
        print()
        print('```{dot}')
        print(f'{to_dot(trimmed_tree)}')
        print('```')
        print()
        print('... , simple tree T is ...')
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
        untrim_tree(dist_mat, trimmed_tree, gen_node_id, gen_edge_id)
        print()
        print('```{dot}')
        print(f'{to_dot(trimmed_tree)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()

# t = create_graph([['v0','i0',11], ['v1','i0',2], ['v2','i0',10], ['i0','i2',7], ['i2','v3',3], ['i2','v4',4]])
# m = create_distance_matrix([
#     [0,  13, 21, 21, 22, 22],
#     [13, 0,  12, 12, 13, 13],
#     [21, 12, 0,  20, 21, 21],
#     [21, 12, 20, 0,  7,  13],
#     [22, 13, 21, 7,  0,  14],
#     [22, 13, 21, 13, 14, 0 ]
# ])
# 
# _next_edge_id = 0
# def gen_edge_id():
#     global _next_edge_id
#     _next_edge_id += 1
#     return f'E{_next_edge_id}'
#
# _next_node_id = 0
# def gen_node_id():
#     global _next_node_id
#     _next_node_id += 1
#     return f'N{_next_node_id}'
#
# untrim_tree(m, t, gen_node_id, gen_edge_id)