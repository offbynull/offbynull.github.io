from collections import Counter
from itertools import product, combinations

from distance_matrix.DistanceMatrix import DistanceMatrix
from graph.UndirectedGraph import Graph
from helpers.Utils import slide_window


def find_nodes_between_leaves(g: Graph, n: str, end_n: str, n_walk: list[str]):
    n_walk.append(n)
    if n == end_n:
        return True
    for e in g.get_outputs(n):
        n1, n2, _ = g.get_edge(e)
        if len(n_walk) >= 2 and {n1, n2} == {n_walk[-1], n_walk[-2]}:
            continue
        next_n = next(iter({n1, n2}.difference({n})))
        done = find_nodes_between_leaves(g, next_n, end_n, n_walk)
        if done:
            return True
    n_walk.pop()


def find_edges_between_leaves(g: Graph, n: str, end_n: str):
    edges = []
    nodes = []
    find_nodes_between_leaves(g, n, end_n, nodes)
    for (n1, n2), _ in slide_window(nodes, 2):
        found_edge = None
        for edge_id in g.get_outputs(n1):
            _end1, _end2, _ed = g.get_edge(edge_id)
            if n2 not in {_end1, _end2}:
                continue
            if found_edge is not None:
                raise ValueError(f'Multiple edges to same node not allowed: {n1, n2}')
            found_edge = edge_id
        if found_edge is None:
            raise ValueError(f'No edge found: {n1, n2}')
        edges.append(found_edge)
    return edges


g = Graph()
# g.insert_node('v1')
# g.insert_node('v2')
# g.insert_node('v3')
# g.insert_node('v4')
# g.insert_node('i0')
# g.insert_node('i1')
# g.insert_edge('v1-i0', 'v1', 'i0', 11.0)
# g.insert_edge('v2-i0', 'v2', 'i0', 2.0)
# g.insert_edge('v3-i1', 'v3', 'i1', 10.0)
# g.insert_edge('v4-i1', 'v4', 'i1', 7.0)
# g.insert_edge('i0-i1', 'i0', 'i1', 7.0)
g.insert_node('v0')
g.insert_node('v1')
g.insert_node('v2')
g.insert_node('v3')
g.insert_node('v4')
g.insert_node('v5')
g.insert_node('i0')
g.insert_node('i1')
g.insert_node('i2')
g.insert_edge('v0-i0', 'v0', 'i0', 11.0)
g.insert_edge('v1-i0', 'v1', 'i0', 2.0)
g.insert_edge('v2-i0', 'v2', 'i0', 10.0)
g.insert_edge('v5-i1', 'v5', 'i1', 7.0)
g.insert_edge('v4-i2', 'v4', 'i2', 4.0)
g.insert_edge('v3-i2', 'v3', 'i2', 3.0)
g.insert_edge('i0-i1', 'i0', 'i1', 4.0)
g.insert_edge('i1-i2', 'i1', 'i2', 3.0)
dm = DistanceMatrix.create_from_graph(g)
print(f'{dm}')


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


print(f'{neighbour_joining_matrix(dm)}')


def count_edges_walked(test_leaf):
    counter = Counter()
    for leaf in dm.leaf_ids_it():
        if leaf == test_leaf:
            continue
        edges = find_edges_between_leaves(g, leaf, test_leaf)
        counter.update(edges)
    return counter


def process(n1, n2, leaf_count):
    n1_edge_counts = sorted(count_edges_walked(n1).most_common())
    n1_edge_counts_total = sum(e[1] for e in n1_edge_counts)
    n2_edge_counts = sorted(count_edges_walked(n2).most_common())
    n2_edge_counts_total = sum(e[1] for e in n2_edge_counts)
    tot_edge_counts = [(n1_e, n1_c + n2_c) for (n1_e, n1_c), (n2_e, n2_c) in zip(n1_edge_counts, n2_edge_counts)]
    tot_edge_counts_total = sum(e[1] for e in tot_edge_counts)
    edges_between_n1_and_n2 = find_edges_between_leaves(g, n1, n2)
    norm_tot_edge_counts = []
    for e, c in tot_edge_counts:
        if e in edges_between_n1_and_n2:
            norm_tot_edge_counts.append((e, c - (leaf_count - 2)))
        else:
            norm_tot_edge_counts.append((e, c))
    norm_tot_edge_counts_total = sum(e[1] for e in norm_tot_edge_counts)
    print(f'{n1=} {n2=}')
    print(f'  {n1_edge_counts} -- total of {n1_edge_counts_total}   FROM {n1}')
    print(f'  {n2_edge_counts} -- total of {n2_edge_counts_total}   FROM {n2}')
    print(f'  {tot_edge_counts} -- total of {tot_edge_counts_total}   {n1} + {n2}')
    print(f'  {norm_tot_edge_counts} -- total of {norm_tot_edge_counts_total}   {n1} + {n2} NORM')


leaf_count = sum(1 for n in g.get_nodes() if n.startswith('v'))
print(f'WHEN LEAF NODES ARE NEIGHBOURS')
print('----------------------')
for n1, n2 in combinations(g.get_nodes(), r=2):
    if n1 == n2:
        continue
    if not(n1.startswith('v') and n2.startswith('v')):
        continue
    edge_id_n1, parent_n1 = [(e, n) for e in g.get_outputs(n1) for n in g.get_edge_ends(e) if n != n1][0]
    edge_id_n2, parent_n2 = [(e, n) for e in g.get_outputs(n2) for n in g.get_edge_ends(e) if n != n2][0]
    if parent_n1 != parent_n2:
        continue
    process(n1, n2, leaf_count)
print()
print(f'WHEN LEAF NODES ARE NOT NEIGHBOURS')
print('----------------------')
for n1, n2 in combinations(g.get_nodes(), r=2):
    if n1 == n2:
        continue
    if not(n1.startswith('v') and n2.startswith('v')):
        continue
    edge_id_n1, parent_n1 = [(e, n) for e in g.get_outputs(n1) for n in g.get_edge_ends(e) if n != n1][0]
    edge_id_n2, parent_n2 = [(e, n) for e in g.get_outputs(n2) for n in g.get_edge_ends(e) if n != n2][0]
    if parent_n1 == parent_n2:
        continue
    process(n1, n2, leaf_count)
print()
print(f'Notice c_all\'s pattern: There number of internal edges are INCONSISTENT and ALWAYS MORE than if the leaf nodes were neighbours')

print('Why? If they aren\'t neighbours, when you calculate the distance between them they\'ll ALWAYS travels one or more internal edges')
print('For example, if v2 and v5 were picked to test if they are neighbours, the path between v2 and v5 travels over 1 internal edge')
print('For example, if v0 and v1 were picked to test if they are neighbours, the path between v0 and v1 travels over NO internal edges')
print('Other than that, the total edge walked counts to all other leaf nodes remain the same')