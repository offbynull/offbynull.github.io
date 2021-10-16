from __future__ import annotations

from itertools import product
from sys import stdin

from distance_matrix.DistanceMatrix import DistanceMatrix
from graph.UndirectedGraph import Graph
from helpers.InputUtils import str_to_list
from phylogeny.UntrimTree import create_distance_matrix


def to_dot(g: Graph) -> str:
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
    def __init__(self, dist_mat: DistanceMatrix):
        self._clusters: dict[str, set[str]] = {}
        self._active: set[str] = set()
        for n in dist_mat.leaf_ids_it():
            self._clusters[n] = {n}
            self._active.add(n)

    def merge(self, c_new: str, c1: str, c2: str) -> None:
        if c1 not in self._clusters or c2 not in self._clusters:
            raise ValueError('???')
        self._clusters[c_new] = self._clusters[c1] | self._clusters[c2]
        self._active.remove(c1)
        self._active.remove(c2)
        self._active.add(c_new)

    def active(self) -> set[str]:
        return self._active.copy()

    def active_count(self) -> int:
        return len(self._active)

    def __getitem__(self, c: str) -> set[str]:
        return self._clusters[c].copy()

    def __str__(self):
        return f'cluster_active={self._active}\ncluster_all   ={self._clusters}'


# MARKDOWN_DIST
def cluster_dist(dm_orig: DistanceMatrix, c_set: ClusterSet, c1: str, c2: str) -> float:
    c1_set = c_set[c1]  # this should be a set of leaf nodes from the ORIGINAL unmodified distance matrix
    c2_set = c_set[c2]  # this should be a set of leaf nodes from the ORIGINAL unmodified distance matrix
    numerator = sum(dm_orig[i, j] for i, j in product(c1_set, c2_set))  # sum it all up
    denominator = len(c1_set) * len(c2_set)  # number of additions that occurred
    return numerator / denominator
# MARKDOWN_DIST


# MARKDOWN
def find_clusters_with_min_dist(dm: DistanceMatrix, c_set: ClusterSet) -> tuple[str, str, float]:
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
        dm: DistanceMatrix,
        dm_orig: DistanceMatrix,
        c_set: ClusterSet,
        old_id1: str,
        old_id2: str,
        new_id: str
) -> None:
    c_set.merge(new_id, old_id1, old_id2)  # create new cluster w/ elements from old - old_ids deactived+new_id actived
    new_dists = {}
    for existing_id in dm.leaf_ids():
        if existing_id == old_id1 or existing_id == old_id2:
            continue
        new_dist = cluster_dist(dm_orig, c_set, new_id, existing_id)
        new_dists[existing_id] = new_dist
    dm.merge(new_id, old_id1, old_id2, new_dists)  # remove old ids and replace with new_id that has new distances


def upgma(dm: DistanceMatrix) -> tuple[Graph, str]:
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
        cluster_merge(dm, dm_orig, c_set, min_n1_id, min_n2_id, f'C{new_node_id}')
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
    return g, root_id
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
        print('Given the distance matrix ...')
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
        print(f'... the UPGMA generated tree is ...')
        print()
        tree, _ = upgma(dist_mat)
        print()
        print('```{dot}')
        print(f'{to_dot(tree)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
