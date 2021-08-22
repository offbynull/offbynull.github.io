from collections import Counter
from typing import TypeVar

from graph.UndirectedGraph import Graph
from helpers.Utils import slide_window

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')
ED = TypeVar('ED')


def find_nodes_between_leaves(g: Graph, n: N, end_n: N, n_walk: list[N]):
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


def path(g: Graph, n: N, end_n: N) -> list[E]:
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


def get_leaf_nodes(g: Graph[N, ND, E, ED]) -> list[N]:
    return [n for n in g.get_nodes() if len(tuple(g.get_outputs(n))) == 1]


def get_leaf_count(g: Graph[N, ND, E, ED]) -> len:
    return len(get_leaf_nodes(g))


# MARKDOWN_COUNT
def count(g: Graph, leaf: N) -> Counter[E]:
    counter = Counter()
    leaf_list = get_leaf_nodes(g)
    leaf_list.remove(leaf)
    for other_leaf in leaf_list:
        edges = path(g, leaf, other_leaf)
        counter.update(edges)
    return counter
# MARKDOWN_COUNT


# MARKDOWN_COMBINE_COUNT
def combined_count(g: Graph, leaf1: N, leaf2: N) -> Counter[E]:
    leaf1_counts = count(g, leaf1)
    leaf2_counts = count(g, leaf2)
    return leaf1_counts + leaf2_counts
# MARKDOWN_COMBINE_COUNT


# MARKDOWN_NORMALIZED_COMBINE_COUNT
def normalized_combined_count(g: Graph, leaf1: N, leaf2: N) -> Counter[E]:
    leaf_count = get_leaf_count(g)
    edge_counts = combined_count(g, leaf1, leaf2)
    path_edges = path(g, leaf1, leaf2)
    for edge in path_edges:
        edge_counts[edge] -= leaf_count - 2
    return edge_counts
# MARKDOWN_NORMALIZED_COMBINE_COUNT


if __name__ == '__main__':
    g = Graph()
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
    print(f'{count_to_all(g, "v0")}')