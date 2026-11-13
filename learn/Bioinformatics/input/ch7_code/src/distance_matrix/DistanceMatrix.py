from __future__ import annotations

from copy import deepcopy
from itertools import product
from typing import Iterator, TypeVar, Generic

from graph import UndirectedGraph
from helpers.Utils import slide_window

ID = TypeVar('ID')


class DistanceMatrix(Generic[ID]):
    def __init__(self, initial: dict[tuple[ID, ID], float]):
        d = {}
        ids = {id for id_pair in initial.keys() for id in id_pair}
        for id1, id2 in product(ids, repeat=2):
            opt1 = (id1, id2) in initial
            opt2 = (id2, id1) in initial
            if id1 == id2:
                if opt1 and initial[(id1, id2)] != 0:
                    raise ValueError(f'Distance to self must be 0 or not provided -- it will always default to 0: {(id1, id2)}')
                continue
            if opt1 and opt2 and initial[(id1, id2)] != initial[(id2, id1)]:
                raise ValueError(f'Distance between leaf nodes inserted twice but distances are not the same: {(id1, id2)} / {(id2, id1)}')
            if opt1:
                dist = initial[(id1, id2)]
            elif opt2:
                dist = initial[(id2, id1)]
            else:
                raise ValueError(f'Expected distance for {(id1, id2)}')
            id1, id2 = sorted([id1, id2])
            d[(id1, id2)] = dist
        for id in ids:
            d[(id, id)] = 0.0
        self._data = d
        self._keys = ids

    def delete(self, id: ID):
        if id not in self._keys:
            raise ValueError(f'{id} does not already exists')
        dels = []
        for i1, i2 in self._data.keys():
            if i1 == id or i2 == id:
                dels.append((i1, i2))
        for key in dels:
            del self._data[key]
        self._keys.remove(id)

    def insert(self, new_id: ID, distances: dict[ID, float]) -> None:
        if new_id in self._keys:
            raise ValueError(f'{new_id} already exists')
        for k in self._keys:
            if k not in distances:
                raise ValueError(f'{k} missing')
        for other_id in self._keys:
            i1, i2 = sorted((new_id, other_id))
            self._data[(i1, i2)] = distances[other_id]
        self._data[new_id, new_id] = 0.0
        self._keys.add(new_id)

    def merge(self, new_id: ID, old_id1: ID, old_id2: ID, distances: dict[ID, float]) -> None:
        self.delete(old_id1)
        self.delete(old_id2)
        return self.insert(new_id, distances)

    def leaf_ids(self) -> set[ID]:
        return self._keys.copy()

    def leaf_ids_it(self) -> Iterator[ID]:
        return iter(self._keys)

    def copy(self) -> DistanceMatrix:
        return deepcopy(self)

    @property
    def n(self):
        return len(self._keys)

    def __getitem__(self, key: tuple[ID, ID]) -> float:
        i1, i2 = sorted(key)
        return self._data[(i1, i2)]

    def __setitem__(self, key: tuple[ID, ID], value: float):
        i1, i2 = sorted(key)
        if i1 == i2:
            raise ValueError('dist to self is always 0.0')
        self._data[(i1, i2)] = value

    def __str__(self) -> str:
        ret = '       '
        for i1 in sorted(self._keys):
            ret += f'{i1}'.ljust(7, ' ')
        ret += '\n'
        for i1 in sorted(self._keys):
            ret += f'{i1}'.ljust(7, ' ')
            for i2 in sorted(self._keys):
                entry = tuple(sorted((i1, i2)))
                ret += f'{self[entry]}'.ljust(7, ' ')
            ret += '\n'
        return ret[:-1]

    @staticmethod
    def create_from_matrix(m: list[list[float]]) -> DistanceMatrix:
        d = {}
        for i in range(len(m)):
            for j in range(len(m)):
                i1, i2 = sorted([i, j])
                d[(i1, i2)] = float(m[i1][i2])
        return DistanceMatrix(d)

    @staticmethod
    def create_from_graph(g: UndirectedGraph.Graph) -> DistanceMatrix:
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
        dists = {}
        for l1, l2 in product(leaf_nodes, repeat=2):
            if l1 == l2:
                continue
            path = []
            find_path_in_tree_between_leaves(g, l1, l2, path)
            path_dist = sum_path(g, path)
            dists[l1, l2] = path_dist
        return DistanceMatrix(dists)