from enum import Enum
from io import BytesIO
from itertools import product
from tkinter import Label, BOTH
from tkinter.ttk import Frame

import pydotplus as pydot
from PIL import Image, ImageTk

from graph import UndirectedGraph
from helpers.Utils import slide_window


#
# DEBUG FUNCTIONS
#
def to_graphviz(g: UndirectedGraph.Graph):
    dg = pydot.Graph()
    for n in g.get_nodes():
        dg.add_node(pydot.Node(f'{n}'))
    for e in g.get_edges():
        n1, n2 = g.get_edge_ends(e)
        dg.add_edge(pydot.Edge(f'{n1}', f'{n2}', label=f'{g.get_edge_data(e)}'))
    dgg = pydot.graph_from_dot_data(dg.to_string())
    f = Frame()
    f.pack(fill=BOTH, expand=1)
    label1 = Label(f)
    label1.photo = ImageTk.PhotoImage(
        Image.open(BytesIO(dgg.create_png()))
    )
    label1.config(image=label1.photo)
    label1.pack(fill=BOTH, expand=1)
    f.mainloop()


def to_dist_matrix(g: UndirectedGraph.Graph) -> [[int]]:
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
    dist_mat = [[0] * len(leaf_nodes) for _ in range(len(leaf_nodes))]
    for l1, l2 in product(leaf_nodes, repeat=2):
        path = []
        find_path_in_tree_between_leaves(g, l1, l2, path)
        path_dist = sum_path(g, path)
        dist_mat[int(l1)][int(l2)] = path_dist
    return dist_mat


#
# ACTUAL CODE STARTS HERE
#
def calc_limb_length(d: [[int]], leaf_idx: int):
    d_len = len(d)
    min_limb_len = None
    for i, k in product(range(d_len), range(d_len)):
        if i == leaf_idx or k == leaf_idx:
            continue
        limb_len = (d[i][leaf_idx] + d[k][leaf_idx] - d[i][k]) // 2
        if min_limb_len is None or limb_len < min_limb_len:
            min_limb_len = limb_len
    return min_limb_len


def to_bald_matrix(d: [[int]], limb_len: int) -> [[int]]:
    d = [r[:] for r in d]
    n = len(d)
    for i in range(n - 1):
        d[n - 1][i] -= limb_len
        d[i][n - 1] -= limb_len
    return d


def to_trimmed_matrix(d: [[int]]) -> [[int]]:
    return [r[:-1] for r in d[:-1]]


def find_additive_distance(d: [[int]]) -> (int, int, int):
    n = len(d) - 1
    for i, k in product(range(n), range(n)):
        if i == k:
            continue
        if d[i][k] == d[i][n] + d[n][k]:
            return i, k, n
    raise ValueError('???')


def find_path(g: UndirectedGraph.Graph, n: str, end_n: str, edges: list[str]):
    for e in g.get_outputs(n):
        if edges and edges[-1] == e:
            continue
        edges.append(e)
        n1, n2, _ = g.get_edge(e)
        if end_n in {n1, n2}:
            return True
        next_n = next(iter({n1, n2}.difference({n})))
        done = find_path(g, next_n, end_n, edges)
        if done:
            return True
    edges.pop()


class SumPathCheckRes(Enum):
    BREAK = 'BREAK',
    ATTACH = 'ATTACH',


def sum_path_check(g: UndirectedGraph.Graph, limit: int, edges: list[str], start_node: str):
    to_node = start_node
    sum = 0
    for e_idx, e in enumerate(edges):
        to_node = next(iter(set(g.get_edge_ends(e)).difference({f'{to_node}'})))
        sum += g.get_edge_data(e)
        if sum == limit:
            return SumPathCheckRes.ATTACH, to_node
        elif sum > limit:
            return SumPathCheckRes.BREAK, to_node, e_idx, sum
    return SumPathCheckRes.BREAK, to_node, len(edges) - 1, sum


def sum_path(g: UndirectedGraph.Graph, edges: list[str]):
    r = 0
    for e in edges:
        r += g.get_edge_data(e)
    return r


class WrappedInt:
    def __init__(self, start=0):
        self.i = start

    def next(self):
        ret = self.i
        self.i += 1
        return ret


def additive_phylogeny(d: [[int]], counter: WrappedInt):
    if len(d) == 2:
        g = UndirectedGraph.Graph()
        g.insert_node('0')
        g.insert_node('1')
        g.insert_edge('0-1', '0', '1', d[0][1])
        return g
    n = len(d) - 1
    limb_len = calc_limb_length(d, n)
    bald_d = to_bald_matrix(d, limb_len)
    i, k, attachment_node = find_additive_distance(bald_d)
    x = bald_d[i][n]
    trimmed_d = to_trimmed_matrix(bald_d)
    t = additive_phylogeny(trimmed_d, counter)
    # to_graphviz(t)
    edges_between_i_and_k = []
    find_path(t, f'{i}', f'{k}', edges_between_i_and_k)
    res = sum_path_check(t, x, edges_between_i_and_k, i)
    op = res[0]
    if op == SumPathCheckRes.BREAK:
        to_node = res[1]
        edge_to_break_idx = res[2]
        edge_to_break = edges_between_i_and_k[edge_to_break_idx]
        edge_to_break_sum = res[3]  # includes edge_to_break weight
        internal_node = f'{counter.next()}'
        weight_to_internal_node = t.get_edge_data(edge_to_break) - (edge_to_break_sum - x)
        weight_to_existing_node = edge_to_break_sum - x
        weight_to_n = limb_len
        from_node = next(iter(set(t.get_edge_ends(edge_to_break)).difference({to_node})))  # get end that isn't to
        t.insert_node(internal_node)
        t.delete_edge(edge_to_break)
        t.insert_edge(f'{from_node}-{internal_node}', f'{from_node}', internal_node, weight_to_internal_node)
        t.insert_edge(f'{internal_node}-{to_node}', internal_node, f'{to_node}', weight_to_existing_node)
        t.insert_node(f'{n}')
        t.insert_edge(f'{internal_node}-{n}', internal_node, f'{n}', weight_to_n)
        return t
    elif op == SumPathCheckRes.ATTACH:
        attach_node = res[1]
        t.insert_node(f'{n}')
        t.insert_edge(f'{attach_node}-{n}', f'{attach_node}', f'{n}', limb_len)
        return t
    raise ValueError('???')


with open('/home/user/Downloads/dataset_240337_6(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

g = UndirectedGraph.Graph()

lines = [s.strip() for s in data.strip().split('\n')]
mat_size = int(lines[0])
dist_mat = [[int(e) for e in row.split()] for row in lines[1:]]

# dist_mat = [
#     [0, 3, 4, 5],
#     [3, 0, 5, 6],
#     [4, 5, 0, 7],
#     [5, 6, 7, 0],
# ]
# dist_mat = [
#     [0, 3, 4, 5, 6],
#     [3, 0, 5, 6, 7],
#     [4, 5, 0, 7, 8],
#     [5, 6, 7, 0, 9],
#     [6, 7, 8, 9, 0]
# ]
# dist_mat = [
#     [0, 13, 21, 22],
#     [13, 0, 12, 13],
#     [21, 12, 0, 13],
#     [22, 13, 13, 0],
# ]
# dist_mat = [
#     [0, 3, 4, 5, 4, 5],
#     [3, 0, 5, 6, 5, 6],
#     [4, 5, 0, 7, 6, 7],
#     [5, 6, 7, 0, 7, 8],
#     [4, 5, 6, 7, 0, 3],
#     [5, 6, 7, 8, 3, 0],
# ]
# dist_mat = [
#     [0, 3, 4, 5, 5, 5, 5],
#     [3, 0, 5, 6, 6, 6, 6],
#     [4, 5, 0, 7, 7, 7, 7],
#     [5, 6, 7, 0, 8, 8, 8],
#     [5, 6, 7, 8, 0, 4, 4],
#     [5, 6, 7, 8, 4, 0, 2],
#     [5, 6, 7, 8, 4, 2, 0],
# ]

# in_g = UndirectedGraph.Graph()
# in_g.insert_node('0')
# in_g.insert_node('1')
# in_g.insert_node('2')
# in_g.insert_node('3')
# in_g.insert_node('4')
# in_g.insert_node('5')
# in_g.insert_node('6')
# in_g.insert_node('7')
# in_g.insert_node('8')
# in_g.insert_node('9')
# in_g.insert_edge('0-7', '0', '7', 1)
# in_g.insert_edge('1-7', '1', '7', 2)
# in_g.insert_edge('2-7', '2', '7', 3)
# in_g.insert_edge('3-7', '3', '7', 4)
# in_g.insert_edge('7-8', '7', '8', 2)
# in_g.insert_edge('8-4', '8', '4', 2)
# in_g.insert_edge('8-9', '8', '9', 1)
# in_g.insert_edge('9-5', '9', '5', 1)
# in_g.insert_edge('9-6', '9', '6', 1)
# to_graphviz(in_g)
# dist_mat = to_dist_matrix(in_g)


graph = additive_phylogeny(dist_mat, WrappedInt(len(dist_mat)))
# to_graphviz(graph)
to_dist_matrix(g)
output = []
for e in graph.get_edges():
    n1, n2 = graph.get_edge_ends(e)
    weight = graph.get_edge_data(e)
    output.append((int(n1), int(n2), weight))
    output.append((int(n2), int(n1), weight))
output.sort()
for n1, n2, weight in output:
    print(f'{n1}->{n2}:{weight}')