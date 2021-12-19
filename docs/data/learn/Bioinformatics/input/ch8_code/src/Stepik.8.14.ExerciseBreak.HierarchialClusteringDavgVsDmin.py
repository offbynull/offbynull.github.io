# Exercise Break: Apply HierarchicalClustering to the distance matrix in the figure below using D_avg instead of D_min.
#
#    , g1  , g2  , g3  , g4  , g5  , g6  , g7  , g8  , g9  , g10
# g1 ,  0.0,  8.1,  9.2,  7.7,  9.3,  2.3,  5.1, 10.2,  6.1,  7.0
# g2 ,  8.1,  0.0, 12.0,  0.9, 12.0,  9.5, 10.1, 12.8,  2.0,  1.0
# g3 ,  9.2, 12.0,  0.0, 11.2,  0.7, 11.1,  8.1,  1.1, 10.5, 11.5
# g4 ,  7.7,  0.9, 11.2,  0.0, 11.2,  9.2,  9.5, 12.0,  1.6,  1.1
# g5 ,  9.3, 12.0,  0.7, 11.2,  0.0, 11.2,  8.5,  1.0, 10.6, 11.6
# g6 ,  2.3,  9.5, 11.1,  9.2, 11.2,  0.0,  5.6, 12.1,  7.7,  8.5
# g7 ,  5.1, 10.1,  8.1,  9.5,  8.5,  5.6,  0.0,  9.1,  8.3,  9.3
# g8 , 10.2, 12.8,  1.1, 12.0,  1.0, 12.1,  9.1,  0.0, 11.4, 12.4
# g9 ,  6.1,  2.0, 10.5,  1.6, 10.6,  7.7,  8.3, 11.4,  0.0,  1.1
# g10,  7.0,  1.0, 11.5,  1.1, 11.6,  8.5,  9.3, 12.4,  1.1,  0.0


# MY ANSWER
# ---------
# This is the same code as the hierarchical clustering code challenge, with some modifications to introduce D_min.
# Recall that the ...
#   * D_min between clusters C1 and C2 compares the distances between all points and chooses the minimum
#   * D_avg between clusters C1 and C2 is the standard UPGMA "average" distance.
from __future__ import annotations

from copy import deepcopy
from itertools import product
from math import dist
from typing import TypeVar, Iterator, Generic, Callable

from graph import UndirectedGraph
from graph.UndirectedGraph import Graph
from helpers.Utils import slide_window




# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE
# EVERYTHING HERE HAS BEEN COPIED FROM CH7 -- DISTANCE MATRIX CODE + UPGMA CODE




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
                d[f'{i1+1}', f'{i2+1}'] = float(m[i1][i2])
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


N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')


def to_dot(g: Graph[N, ND, E, float]) -> str:
    ret = 'graph G {\n'
    ret += ' graph[rankdir=BT]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = sorted(g.get_nodes())
    for n in nodes:
        weight = g.get_node_data(n)
        ret += f'{n} [label="{n}\\n{weight}"]\n'
    for e in sorted(g.get_edges()):
        n1, n2, weight = g.get_edge(e)
        ret += f'{n1} -- {n2} [label="{weight}"]\n'
    ret += '}'
    return ret


class ClusterSet:
    def __init__(self, dist_mat: DistanceMatrix[N]):
        self._clusters: dict[str, set[str]] = {}
        self._active: set[str] = set()
        for n in dist_mat.leaf_ids_it():
            self._clusters[n] = {n}
            self._active.add(n)

    def merge(self, c_new: N, c1: N, c2: N) -> None:
        if c1 not in self._clusters or c2 not in self._clusters:
            raise ValueError('???')
        self._clusters[c_new] = self._clusters[c1] | self._clusters[c2]
        self._active.remove(c1)
        self._active.remove(c2)
        self._active.add(c_new)

    def active(self) -> set[N]:
        return self._active.copy()

    def active_count(self) -> int:
        return len(self._active)

    def __getitem__(self, c: N) -> set[N]:
        return self._clusters[c].copy()

    def __str__(self):
        return f'cluster_active={self._active}\ncluster_all   ={self._clusters}'


def cluster_dist_avg(dm_orig: DistanceMatrix[N], c_set: ClusterSet, c1: str, c2: str) -> float:
    c1_set = c_set[c1]  # this should be a set of leaf nodes from the ORIGINAL unmodified distance matrix
    c2_set = c_set[c2]  # this should be a set of leaf nodes from the ORIGINAL unmodified distance matrix
    numerator = sum(dm_orig[i, j] for i, j in product(c1_set, c2_set))  # sum it all up
    denominator = len(c1_set) * len(c2_set)  # number of additions that occurred
    return numerator / denominator


def cluster_dist_min(dm_orig: DistanceMatrix[N], c_set: ClusterSet, c1: str, c2: str) -> float:
    c1_set = c_set[c1]  # this should be a set of leaf nodes from the ORIGINAL unmodified distance matrix
    c2_set = c_set[c2]  # this should be a set of leaf nodes from the ORIGINAL unmodified distance matrix
    return min(dm_orig[i, j] for i, j in product(c1_set, c2_set))


def find_clusters_with_min_dist(dm: DistanceMatrix[N], c_set: ClusterSet) -> tuple[N, N, float]:
    assert c_set.active_count() > 1
    min_n1_id = None
    min_n2_id = None
    min_dist = None
    for n1, n2 in product(c_set.active(), repeat=2):
        if n1 == n2:
            continue
        d = dm[n1, n2]
        if min_dist is None or d < min_dist:
            min_n1_id = n1
            min_n2_id = n2
            min_dist = d
    assert min_n1_id is not None and min_n2_id is not None and min_dist is not None
    return min_n1_id, min_n2_id, min_dist


def cluster_merge(
        dm: DistanceMatrix[N],
        dm_orig: DistanceMatrix[N],
        c_set: ClusterSet,
        old_id1: N,
        old_id2: N,
        new_id: N,
        cluster_dist_func: Callable[[DistanceMatrix[N], ClusterSet, str, str], float]
) -> None:
    c_set.merge(new_id, old_id1, old_id2)  # create new cluster w/ elements from old - old_ids deactived+new_id actived
    new_dists = {}
    for existing_id in dm.leaf_ids():
        if existing_id == old_id1 or existing_id == old_id2:
            continue
        new_dist = cluster_dist_func(dm_orig, c_set, new_id, existing_id)
        new_dists[existing_id] = new_dist
    dm.merge(new_id, old_id1, old_id2, new_dists)  # remove old ids and replace with new_id that has new distances


def upgma(
        dm: DistanceMatrix[N],
        cluster_dist_func: Callable[[DistanceMatrix[N], ClusterSet, str, str], float]
) -> tuple[Graph, N, ClusterSet]:
    g = Graph()
    c_set = ClusterSet(dm)  # primed with leaf nodes (all active)
    for node in dm.leaf_ids_it():
        g.insert_node(node, 0)  # initial node weights (each leaf node has an age of 0)
    dm_orig = dm.copy()
    # set node ages
    next_node_id = 0
    next_edge_id = 0
    while c_set.active_count() > 1:
        min_n1_id, min_n2_id, min_dist = find_clusters_with_min_dist(dm, c_set)
        new_node_id = next_node_id
        new_node_age = min_dist / 2
        g.insert_node(f'C{new_node_id}', new_node_age)
        next_node_id += 1
        g.insert_edge(f'E{next_edge_id}', min_n1_id, f'C{new_node_id}')
        next_edge_id += 1
        g.insert_edge(f'E{next_edge_id}', min_n2_id, f'C{new_node_id}')
        next_edge_id += 1
        cluster_merge(dm, dm_orig, c_set, min_n1_id, min_n2_id, f'C{new_node_id}', cluster_dist_func)
    # set amount of age added by each edge
    nodes_by_age = sorted([(n, g.get_node_data(n)) for n in g.get_nodes()], key=lambda x: x[1])
    set_edges = set()  # edges that have already had their weights set
    for child_n, child_age in nodes_by_age:
        for e in g.get_outputs(child_n):
            if e in set_edges:
                continue
            parent_n = [n for n in g.get_edge_ends(e) if n != child_n].pop()
            parent_age = g.get_node_data(parent_n)
            weight = parent_age - child_age
            g.update_edge_data(e, weight)
            set_edges.add(e)
    root_id = c_set.active().pop()
    return g, root_id, c_set





dm_str = '''
   , g1  , g2  , g3  , g4  , g5  , g6  , g7  , g8  , g9  , g10
g1 ,  0.0,  8.1,  9.2,  7.7,  9.3,  2.3,  5.1, 10.2,  6.1,  7.0
g2 ,  8.1,  0.0, 12.0,  0.9, 12.0,  9.5, 10.1, 12.8,  2.0,  1.0
g3 ,  9.2, 12.0,  0.0, 11.2,  0.7, 11.1,  8.1,  1.1, 10.5, 11.5
g4 ,  7.7,  0.9, 11.2,  0.0, 11.2,  9.2,  9.5, 12.0,  1.6,  1.1
g5 ,  9.3, 12.0,  0.7, 11.2,  0.0, 11.2,  8.5,  1.0, 10.6, 11.6
g6 ,  2.3,  9.5, 11.1,  9.2, 11.2,  0.0,  5.6, 12.1,  7.7,  8.5
g7 ,  5.1, 10.1,  8.1,  9.5,  8.5,  5.6,  0.0,  9.1,  8.3,  9.3
g8 , 10.2, 12.8,  1.1, 12.0,  1.0, 12.1,  9.1,  0.0, 11.4, 12.4
g9 ,  6.1,  2.0, 10.5,  1.6, 10.6,  7.7,  8.3, 11.4,  0.0,  1.1
g10,  7.0,  1.0, 11.5,  1.1, 11.6,  8.5,  9.3, 12.4,  1.1,  0.0
'''.strip()
dm_str_lines = dm_str.split('\n')
dm_str_table = [l.split(',') for l in dm_str_lines]
dm_dict = {}
for i, row in enumerate(dm_str_table):
    for j, cell in enumerate(row):
        if i > 0 and j > 0:
            h_row = dm_str_table[i][0].strip()
            h_col = dm_str_table[0][j].strip()
            val = float(cell.strip())
            dm_dict[h_row, h_col] = val

dist_mat = DistanceMatrix(dm_dict)

print(f'USING D_AVG...')
tree, root, clusters = upgma(dist_mat.copy(), cluster_dist_avg)
for c, v in clusters._clusters.items():
    if not c.startswith('C'):
        continue
    print(' '.join(v))
print(f'{to_dot(tree)}')

print(f'USING D_MIN...')
tree, root, clusters = upgma(dist_mat.copy(), cluster_dist_min)
for c, v in clusters._clusters.items():
    if not c.startswith('C'):
        continue
    print(' '.join(v))
print(f'{to_dot(tree)}')