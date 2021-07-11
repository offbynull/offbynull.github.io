from enum import Enum
from itertools import product

from graph import UndirectedGraph

import pydotplus as pydot
from PIL import Image, ImageTk
from tkinter import Tk, Label, BOTH
from tkinter.ttk import Frame, Style
from io import BytesIO

from helpers.Utils import slide_window

# Since the distance matrix for SARS-like coronaviruses is non-additive, we will cheat a bit and slightly modify it to
# make it additive so that you can apply AdditivePhylogeny to it (see the figure below).
#
# Exercise Break: Construct the simple tree fitting this distance matrix.

# NOTE: This uses the code from the additive phylogeny code challenge.


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


g = UndirectedGraph.Graph()

dist_mat = [
    ['', 'Cow', 'Pig', 'Horse', 'Mouse', 'Dog', 'Cat', 'Turkey', 'Civet', 'Human'],
    ['Cow', 0, 295, 306, 497, 1081, 1091, 1003, 956, 954],
    ['Pig', 295, 0, 309, 500, 1084, 1094, 1006, 959, 957],
    ['Horse', 306, 309, 0, 489, 1073, 1083, 995, 948, 946],
    ['Mouse', 497, 500, 489, 0, 1092, 1102, 1014, 967, 965],
    ['Dog', 1081, 1084, 1073, 1092, 0, 818, 1056, 1053, 1051],
    ['Cat', 1091, 1094, 1083, 1102, 818, 0, 1066, 1063, 1061],
    ['Turkey', 1003, 1006, 995, 1014, 1056, 1066, 0, 975, 973],
    ['Civet', 956, 959, 948, 967, 1053, 1063, 975, 0, 16],
    ['Human', 954, 957, 946, 965, 1051, 1061, 973, 16, 0],
]
dist_mat = dist_mat[1:]
dist_mat = [row[1:] for row in dist_mat]


graph = additive_phylogeny(dist_mat, WrappedInt(len(dist_mat)))
to_graphviz(graph)
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