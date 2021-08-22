from collections import Counter
from itertools import combinations
from typing import TypeVar

from graph.UndirectedGraph import Graph
from helpers.InputUtils import str_to_list
from helpers.Utils import slide_window

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')
ED = TypeVar('ED')


def create_tree(edges: list[list[str, str]]) -> Graph:
    g = Graph()
    for n in {n for e in edges for n in e}:
        g.insert_node(n)
    for n1, n2 in edges:
        g.insert_edge(f'{n1}-{n2}', n1, n2)
    return g


def tree_to_dot(g: Graph) -> str:
    ret = '''
graph G {
 graph[rankdir=LR]
 node[shape=none, fontname="Courier-Bold", fontsize=10, width=0.3, height=0.3, fixedsize=true]
 edge[fontname="Courier-Bold", fontsize=10]
 ranksep=0.25
'''
    nodes = sorted(g.get_nodes())
    for i, n in enumerate(nodes):
        ret += f'{n}\n'
    for e in g.get_edges():
        n1, n2 = g.get_edge_ends(e)
        ret += f'{n1} -- {n2} [label=""]\n'
    ret += '}'
    return ret


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


def get_path(g: Graph, n: N, end_n: N) -> list[E]:
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
def count(g: Graph, leaf_id: N) -> Counter[E]:
    # Collect paths from leaf_id to all other leaf nodes
    path_collection = []
    for other_leaf_id in get_leaf_nodes(g):
        if leaf_id == other_leaf_id:
            continue
        path = get_path(g, leaf_id, other_leaf_id)
        path_collection.append(path)
    # Count edges across all paths
    edge_counts = Counter()
    for path in path_collection:
        edge_counts.update(path)
    # Return edge counts
    return edge_counts
# MARKDOWN_COUNT


def main_count():
    edges, _ = str_to_list(input().strip(), 0)
    g = create_tree(edges)
    print('Edge counts walked from each leaf node...')
    print()
    print('```{dot}')
    print(f'{tree_to_dot(g)}')
    print('```')
    print()
    for leaf in sorted(get_leaf_nodes(g)):
        c = sorted(count(g, leaf).most_common())
        edge_cnt_str = ', '.join(f'{e}:{cnt}' for e, cnt in c)
        print(f' * count({leaf}) = {edge_cnt_str}')


# MARKDOWN_COMBINE_COUNT
def combined_count(g: Graph, leaf1: N, leaf2: N) -> Counter[E]:
    c1 = count(g, leaf1)
    c2 = count(g, leaf2)
    return c1 + c2
# MARKDOWN_COMBINE_COUNT


def main_combine_count():
    edges, _ = str_to_list(input().strip(), 0)
    g = create_tree(edges)
    print('Combined edge counts...')
    print()
    print('```{dot}')
    print(f'{tree_to_dot(g)}')
    print('```')
    print()
    for l1, l2 in combinations(sorted(get_leaf_nodes(g)), r = 2):
        c = sorted(combined_count(g, l1, l2).most_common())
        edge_cnt_str = ', '.join(f'{e}:{cnt}' for e, cnt in c)
        print(f' * count({l1}) + count({l2}) = {edge_cnt_str}')


# MARKDOWN_NORMALIZED_COMBINE_COUNT
def combine_count_and_normalize(g: Graph, leaf1: N, leaf2: N) -> Counter[E]:
    edge_counts = combined_count(g, leaf1, leaf2)
    leaf_count = get_leaf_count(g)
    path_edges = get_path(g, leaf1, leaf2)
    for e in path_edges:
        edge_counts[e] -= leaf_count - 2
    return edge_counts
# MARKDOWN_NORMALIZED_COMBINE_COUNT


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        val = input().strip()
        if val == 'count':
            main_count()
        elif val == 'combined_count':
            main_combine_count()
        else:
            raise ValueError('???')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()