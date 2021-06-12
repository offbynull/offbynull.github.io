import re
from itertools import product

from graph import UndirectedGraph
from helpers.Utils import slide_window

with open('/home/user/Downloads/dataset_240335_12.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

g = UndirectedGraph.Graph()

lines = [s.strip() for s in data.strip().split('\n')]
leaf_count = int(lines[0])
for line in lines[1:]:
    n1, n2, dist = re.split(r'->|:', line)
    if not g.has_node(n1):
        g.insert_node(n1)
    if not g.has_node(n2):
        g.insert_node(n2)
    n1, n2 = sorted([n1, n2])
    e_id = f'{n1}-{n2}'
    if not g.has_edge(e_id):
        g.insert_edge(e_id, n1, n2, int(dist))
    else:
        assert g.get_edge_data(e_id) == int(dist)  # input file is listing edges twice, make sure dupes are the same


def find_path_in_tree_between_leaves(g: UndirectedGraph.Graph, n: str, end_n: str, n_walk: list[str]):
    n_walk.append(n)
    if n == end_n:
        return True
    for e in g.get_outputs(n):
        n1, n2, _ = g.get_edge(e)
        if len(n_walk) >= 2 and {n1, n2} == {n_walk[-1], n_walk[-2]}:
            continue
        next_n = next(iter({n1, n2}.difference({n})))
        done = find_path_in_tree_between_leaves(g, next_n, end_n, n_walk)
        if done:
            return True
    n_walk.pop()


def sum_path(g: UndirectedGraph.Graph, n_walk: list[str]):
    if len(n_walk) == 1:
        return 0
    ret = 0
    for (n1, n2), _ in slide_window(n_walk, 2):
        for e_id in g.get_outputs(n1):
            e_n1, e_n2, dist = g.get_edge(e_id)
            if {n1, n2} == {e_n1, e_n2}:
                ret += dist
    return ret


leaf_nodes = sorted([n for n in g.get_nodes() if g.get_degree(n) == 1])
leaf_node_dists = {}
# print(f'{leaf_nodes}')
# print(f'{g}')
for l1, l2 in product(leaf_nodes, repeat=2):
    path = []
    find_path_in_tree_between_leaves(g, l1, l2, path)
    path_dist = sum_path(g, path)
    leaf_node_dists[(path[0], path[-1])] = path_dist
    # print(f'{path} {path_dist}')

for l1 in leaf_nodes:
    out = []
    for l2 in leaf_nodes:
        out.append(f'{leaf_node_dists[(l1, l2)]}')
    out_str = ' '.join(out)
    print(out_str)
