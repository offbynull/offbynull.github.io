import math
from collections import Counter
from typing import TypeVar, Callable, Any, Optional, Iterable

from graph.UndirectedGraph import Graph

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')
ED = TypeVar('ED')


def create_graph(elems: list[list[Any]]) -> Graph:
    g = Graph()
    for e in elems:
        if e[0] == 'n':
            g.insert_node(e[1], e[2])
        if e[0] == 'e':
            g.insert_edge(f'{e[1]}-{e[2]}', e[1], e[2], {})
    return g


def to_dot(g: Graph) -> str:
    ret = 'graph G {\n'
    ret += ' graph[rankdir=BT]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    nodes = sorted(g.get_nodes())
    for n in nodes:
        seq = g.get_node_data(n)
        ret += f'{n} [label="{n}\\n{seq}"]\n'
    for e in g.get_edges():
        n1, n2, weight = g.get_edge(e)
        ret += f'{n1} -- {n2} [label="{weight.get("w")}"]\n'
    ret += '}'
    return ret


def hamming_distance(e1: str, e2: str):
    if e1 == e2:
        return 0
    else:
        return -1


def populate_distance_sets(
        tree: Graph[N, ND, E, ED],
        seq_length: int,
        get_dist_set: Callable[
            [
                N,   # node
                int  # index within N's sequence
            ],
            Optional[dict[str, float]]  # distance set for that index of N's sequence (None if not set)
        ],
        set_dist_set: Callable[
            [
                N,                 # node
                int,               # index within N's sequence
                dict[str, float]   # distance set for that index of N's sequence
            ],
            None
        ],
        dist_metric: Callable[[str, str], float],
        elem_types: str = 'ACTG'
) -> None:
    # Walk upward from leaf nodes
    pending_nodes = Counter()
    for n in tree.get_nodes():
        pending_nodes[n] = tree.get_degree(n) - 1  # - 1 to ignore the neighbour we're walking up from
    while pending_nodes:
        # Get and remove next node ready to be processed
        n = {n for n, c in pending_nodes.items() if c == 0}.pop()
        del pending_nodes[n]
        # For each index, pull distance sets for outputs of n (that have them) and use them to build a distance
        # set for n.
        for i in range(seq_length):
            child_dist_sets = []
            for n_child in tree.get_outputs(n):
                dist_set = get_dist_set(n_child, i)
                if dist_set is not None:
                    child_dist_sets.append(dist_set)
            dist_set = distance_for_internal_element_types(child_dist_sets, dist_metric, elem_types)
            set_dist_set(n, i, dist_set)
        # Mark neighbours as processed
        for n_neighbour in tree.get_outputs(n):
            if n_neighbour in pending_nodes:
                pending_nodes[n_neighbour] -= 1


# MARKDOWN_INTERNAL_DIST_SET
def distance_for_internal_element_types(
        downstream_dist_sets: Iterable[dict[str, float]],
        dist_metric: Callable[[str, str], float],
        elem_types: str = 'ACTG'
) -> dict[str, float]:
    dist_set = {}
    for elem_type in elem_types:
        weight = distance_for_internal_element_type(elem_type, downstream_dist_sets, dist_metric, elem_types)
        dist_set[elem_type] = weight
    return dist_set


def distance_for_internal_element_type(
        elem_type_dst: str,
        downstream_dist_sets: Iterable[dict[str, float]],
        dist_metric: Callable[[str, str], float],
        elem_types: str = 'ACTG'
) -> float:
    chosen_dists = []
    for downstream_dist_set in downstream_dist_sets:
        possible_dists = []
        for elem_type_src in elem_types:
            possible_dist = downstream_dist_set[elem_type_src] + dist_metric(elem_type_src, elem_type_dst)
            possible_dists.append(possible_dist)
        chosen_dist = min(possible_dists)
        chosen_dists.append(chosen_dist)
    return sum(chosen_dists)
# MARKDOWN_INTERNAL_DIST_SET


# MARKDOWN_LEAF_DIST_SET
def distance_for_leaf_element_types(
        elem_type_dst: str,
        elem_types: str = 'ACTG'
) -> dict[str, float]:
    dist_set = {}
    for e in elem_types:
        if e == elem_type_dst:
            dist_set[e] = 0.0
        else:
            dist_set[e] = math.inf
    return dist_set
# MARKDOWN_LEAF_DIST_SET


r = distance_for_internal_element_types(
    [
        {
            'A': math.inf,
            'C': 0,
            'T': math.inf,
            'G': math.inf
        },
        {
            'A': math.inf,
            'C': 0,
            'T': math.inf,
            'G': math.inf
        }
    ],
    hamming_distance
)
print(f'{r}')


# def main():
#     print("<div style=\"border:1px solid black;\">", end="\n\n")
#     print("`{bm-disable-all}`", end="\n\n")
#     try:
#         elems, _ = str_to_list(input().strip(), 0)
#         g = create_graph(elems)
#         print('The tree...')
#         print()
#         print('```{dot}')
#         print(f'{to_dot(g)}')
#         print('```')
#         print()
#         print('... has a parsimony score of ...')
#         populate_edge_similarity(
#             g,
#             lambda nd: nd,
#             lambda ed, weight: ed.__setitem__('w', weight)
#         )
#         score = parsimony_score(g, lambda ed: ed['w'])
#         print()
#         print(f'{score}')
#         print()
#         print('```{dot}')
#         print(f'{to_dot(g)}')
#         print('```')
#         print()
#     finally:
#         print("</div>", end="\n\n")
#         print("`{bm-enable-all}`", end="\n\n")
#
#
# if __name__ == '__main__':
#     main()