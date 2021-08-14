from __future__ import annotations

from copy import deepcopy
from io import BytesIO
from itertools import product
from tkinter import Label, BOTH
from tkinter.ttk import Frame
from typing import Iterator

import pydotplus as pydot
from PIL import Image, ImageTk

from graph import UndirectedGraph
from helpers.Utils import slide_window


class DistanceMatrix:
    def __init__(self, initial: list[list[float]]):
        d = {}
        for i in range(len(initial)):
            for j in range(len(initial)):
                i1, i2 = sorted([i, j])
                d[(i1, i2)] = float(initial[i1][i2])
        self._data = d
        self._keys = [i for i in range(len(initial))]
        self._next_id = len(self._keys)

    def delete(self, id: int):
        dels = []
        for i1, i2 in self._data.keys():
            if i1 == id or i2 == id:
                dels.append((i1, i2))
        for key in dels:
            del self._data[key]
        self._keys.remove(id)

    def insert(self, distances: dict[int, float]) -> int:
        for k in self._keys:
            if k not in distances:
                raise ValueError(f'{k} missing')
        new_id = self._next_id
        self._next_id += 1
        for other_id in self._keys:
            i1, i2 = sorted((new_id, other_id))
            self._data[(i1, i2)] = distances[other_id]
        self._data[new_id, new_id] = 0.0
        self._keys.append(new_id)
        return new_id

    def merge(self, old_id1: int, old_id2: int, distances: dict[int, float]) -> int:
        self.delete(old_id1)
        self.delete(old_id2)
        return self.insert(distances)

    def leaf_ids(self) -> Iterator[int]:
        return iter(self._keys)

    def copy(self) -> DistanceMatrix:
        return deepcopy(self)

    def ids(self) -> list[int]:
        return self._keys.copy()

    @property
    def n(self):
        return len(self._keys)

    def __getitem__(self, key: tuple[int, int]) -> float:
        i1, i2 = sorted(key)
        return self._data[(i1, i2)]

    def __setitem__(self, key: tuple[int, int], value: float):
        i1, i2 = sorted(key)
        if i1 == i2:
            raise ValueError('dist to self is always 0.0')
        self._data[(i1, i2)] = value

    def __str__(self) -> str:
        ret = '       '
        for i1 in sorted(self._keys):
            ret += f'N{i1}'.ljust(7, ' ')
        ret += '\n'
        for i1 in sorted(self._keys):
            ret += f'N{i1}'.ljust(7, ' ')
            for i2 in sorted(self._keys):
                ret += f'{self[sorted((i1, i2))]}'.ljust(7, ' ')
            ret += '\n'
        return ret[:-1]



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


def to_dist_matrix(g: UndirectedGraph.Graph) -> DistanceMatrix:
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
    return DistanceMatrix(dist_mat)


#
# ACTUAL CODE STARTS HERE
#
def total_distance(dist_mat: DistanceMatrix) -> dict[int, float]:
    ret = {}
    for l1 in dist_mat.leaf_ids():
        ret[l1] = sum(dist_mat[l1, l2] for l2 in dist_mat.leaf_ids())
    return ret


def neighbour_joining_matrix(dist_mat: DistanceMatrix) -> DistanceMatrix:
    tot_dists = total_distance(dist_mat)
    n = dist_mat.n
    ret = dist_mat.copy()
    for l1, l2 in product(dist_mat.leaf_ids(), repeat=2):
        if l1 == l2:
            continue
        ret[l1, l2] = (n - 2) * dist_mat[l1, l2] - tot_dists[l1] - tot_dists[l2]
    return ret


def find_min(nj_mat: DistanceMatrix) -> tuple[int, int]:
    min_l1 = -1
    min_l2 = -1
    for l1, l2 in product(nj_mat.leaf_ids(), repeat=2):
        if l1 == l2:
            continue
        if min_l1 == -1 or nj_mat[min_l1, min_l2] > nj_mat[l1, l2]:
            min_l1 = l1
            min_l2 = l2
    return min_l1, min_l2


def calc_delta(dist_mat: DistanceMatrix, l1: int, l2: int) -> float:
    n = dist_mat.n
    tot_dist = total_distance(dist_mat)
    return (tot_dist[l1] - tot_dist[l2]) / (n - 2)


def consolidate_matrix_entries(dist_mat: DistanceMatrix, l1: int, l2: int) -> int:
    new_dists = {}
    for k in dist_mat.leaf_ids():
        new_dists[k] = 0.5 * (dist_mat[k, l1] + dist_mat[k, l2] - dist_mat[l1, l2])
    new_id = dist_mat.merge(l1, l2, new_dists)
    return new_id


def neighbour_joining_phylogeny(d: DistanceMatrix):
    if d.n == 2:
        g = UndirectedGraph.Graph()
        l1, l2 = d.ids()
        g.insert_node(f'{l1}')
        g.insert_node(f'{l2}')
        g.insert_edge(f'{l1}-{l2}', f'{l1}', f'{l2}', d[l1, l2])
        return g
    nj_mat = neighbour_joining_matrix(d)
    i, j = find_min(nj_mat)
    delta = calc_delta(d, i, j)
    limb_len_i = 0.5 * (d[i, j] + delta)
    limb_len_j = 0.5 * (d[i, j] - delta)
    consolidated_id = consolidate_matrix_entries(d, i, j)
    t = neighbour_joining_phylogeny(d)
    if not t.has_node(consolidated_id):
        t.insert_node(consolidated_id)
    t.insert_node(i)
    t.insert_node(j)
    t.insert_edge('-'.join(sorted([f'{consolidated_id}', f'{i}'])), consolidated_id, i, limb_len_i)
    t.insert_edge('-'.join(sorted([f'{consolidated_id}', f'{j}'])), consolidated_id, j, limb_len_j)
    return t


with open('/home/user/Downloads/dataset_240340_7.txt', mode='r', encoding='utf-8') as f:
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


graph = neighbour_joining_phylogeny(
    DistanceMatrix(dist_mat)
)
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
    print(f'{n1}->{n2}:{weight:.3f}')