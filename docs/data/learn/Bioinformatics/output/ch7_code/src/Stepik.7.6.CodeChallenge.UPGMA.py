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

with open('/home/user/Downloads/dataset_240339_8.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = [s.strip() for s in data.strip().split('\n')]
mat_size = int(lines[0])
dist_mat = [[int(e) for e in row.split()] for row in lines[1:]]



def to_graphviz(g: UndirectedGraph.Graph):
    dg = pydot.Graph()
    for n in g.get_nodes():
        dg.add_node(pydot.Node(f'{n}', label=f'{g.get_node_data(n):.2f}'))
    for e in g.get_edges():
        n1, n2 = g.get_edge_ends(e)
        dg.add_edge(pydot.Edge(f'{n1}', f'{n2}', label=f'{g.get_edge_data(e):.2f}'))
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







class DistanceMatrix:
    def __init__(self, initial: list[list[int]]):
        d = {}
        for i in range(len(initial)):
            for j in range(len(initial)):
                i1, i2 = sorted([i, j])
                d[(i1, i2)] = float(initial[i1][i2])
        self._data = d
        self._keys = {i for i in range(len(initial))}

    def delete(self, id: int):
        dels = []
        for i1, i2 in self._data.keys():
            if i1 == id or i2 == id:
                dels.append((i1, i2))
        for key in dels:
            del self._data[key]
        self._keys.remove(id)

    def insert(self, id: int, distances: dict[int, float]):
        assert distances.keys() == self._keys
        assert id not in self._data
        for other_id in self._keys:
            i1, i2 = sorted((id, other_id))
            self._data[(i1, i2)] = distances[other_id]
        self._data[id, id] = 0.0
        self._keys.add(id)

    def merge(self, old_id1: int, old_id2: int, new_id: int, distances: dict[int, float]):
        self.delete(old_id1)
        self.delete(old_id2)
        self.insert(new_id, distances)

    def leaf_ids(self) -> Iterator[int]:
        return iter(self._keys)

    def copy(self) -> DistanceMatrix:
        return deepcopy(self)

    def ids(self) -> set[int]:
        return self._keys.copy()

    def __getitem__(self, item: tuple[int, int]) -> float:
        i1, i2 = sorted(item)
        return self._data[(i1, i2)]

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


class ClusterSet:
    def __init__(self, original_node_count: int):
        self._clusters: dict[int, set[int]] = {}
        self._active: set[int] = set()
        for i in range(original_node_count):
            self._clusters[i] = {i}
            self._active.add(i)

    def merge(self, c_new: int, c1: int, c2: int) -> None:
        if c1 not in self._clusters or c2 not in self._clusters:
            raise ValueError('???')
        self._clusters[c_new] = self._clusters[c1] | self._clusters[c2]
        self._active.remove(c1)
        self._active.remove(c2)
        self._active.add(c_new)

    def active(self) -> set[int]:
        return self._active.copy()

    def active_count(self) -> int:
        return len(self._active)

    def __getitem__(self, c: int) -> set[int]:
        return self._clusters[c].copy()

    def __str__(self):
        return f'cluster_active={self._active}\ncluster_all   ={self._clusters}'


def cluster_dist(dm_orig: DistanceMatrix, c_set: ClusterSet, c1: int, c2: int) -> float:
    c1_set = c_set[c1]  # this should be a set of leaf nodes from the ORIGINAL unmodified distance matrix
    c2_set = c_set[c2]  # this should be a set of leaf nodes from the ORIGINAL unmodified distance matrix
    numerator = sum(dm_orig[i, j] for i, j in product(c1_set, c2_set))  # sum it all up
    denominator = len(c1_set) * len(c2_set)  # number of additions that occurred
    return numerator / denominator


def find_clusters_with_min_dist(d_mat: DistanceMatrix, c_set: ClusterSet) -> tuple[int, int, float]:
    assert c_set.active_count() > 1
    min_n1_id = None
    min_n2_id = None
    min_dist = None
    for n1, n2 in product(c_set.active(), repeat=2):
        if n1 == n2:
            continue
        d = d_mat[n1, n2]
        # d = cluster_dist(orig_dist_mat, clusters[n1], clusters[n2])
        if min_dist is None or d < min_dist:
            min_n1_id = n1
            min_n2_id = n2
            min_dist = d
    assert min_n1_id is not None and min_n2_id is not None and min_dist is not None
    return min_n1_id, min_n2_id, min_dist


def cluster_merge(d_mat: DistanceMatrix, d_mat_orig: DistanceMatrix, c_set: ClusterSet, old_id1: int, old_id2: int, new_id: int) -> None:
    c_set.merge(new_id, old_id1, old_id2)  # create new cluster w/ elements from old - old_ids deactived+new_id actived
    new_dists = {}
    for existing_id in d_mat.ids():
        if existing_id == old_id1 or existing_id == old_id2:
            continue
        new_dist = cluster_dist(d_mat_orig, c_set, new_id, existing_id)
        new_dists[existing_id] = new_dist
    d_mat.merge(old_id1, old_id2, new_id, new_dists)  # remove old ids and replace with new_id that has new distances


def upgma(d_mat: DistanceMatrix, n: int) -> tuple[UndirectedGraph.Graph, int]:
    d_mat_orig = d_mat.copy()
    g = UndirectedGraph.Graph()
    c_set = ClusterSet(n)  # primed with nodes 0 to n-1 (all activate)
    for node in range(n):
        g.insert_node(node, 0)  # initial node weights (each leaf node has an age of 0)
    next_node_id = n
    next_edge_id = 0
    while c_set.active_count() > 1:
        # print(f'{dist_mat}')
        # print(f'{g}')
        # print(f'{c_set}')
        min_n1_id, min_n2_id, min_dist = find_clusters_with_min_dist(d_mat, c_set)
        # print(f'N{min_n1_id}, N{min_n2_id}, {min_dist}')
        new_node_id = next_node_id
        new_node_age = min_dist / 2
        g.insert_node(new_node_id, new_node_age)
        next_node_id += 1
        g.insert_edge(next_edge_id, min_n1_id, new_node_id)
        next_edge_id += 1
        g.insert_edge(next_edge_id, min_n2_id, new_node_id)
        next_edge_id += 1
        cluster_merge(d_mat, d_mat_orig, c_set, min_n1_id, min_n2_id, new_node_id)
        # print(f'{dist_mat}')
        # print(f'{g}')
        # print(f'{c_set}')
        # print(f'----------')
    for e in set(g.get_edges()):
        n1_id, n2_id, _ = g.get_edge(e)
        deeper_id, shallower_id = sorted([n1_id, n2_id])  # deeper is the closer to bottom of tree (eg. near leaf nodes)
        deeper_age = g.get_node_data(deeper_id)
        shallower_age = g.get_node_data(shallower_id)
        weight = shallower_age - deeper_age
        g.update_edge_data(e, weight)
    root_id = c_set.active().pop()
    return g, root_id


dist_mat = DistanceMatrix(dist_mat)
graph, root = upgma(dist_mat, mat_size)
output = []
for e in graph.get_edges():
    n1, n2 = graph.get_edge_ends(e)
    weight = graph.get_edge_data(e)
    output.append((int(n1), int(n2), weight))
    output.append((int(n2), int(n1), weight))
output.sort()
for n1, n2, weight in output:
    print(f'{n1}->{n2}:{weight:.3f}')
# to_graphviz(graph)
