from typing import TypeVar, Callable, Tuple, Optional, List

from Graph import Graph

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')
ED = TypeVar('ED')
ELEM = TypeVar('ELEM')

def backtrack(
        g: Graph[N, ND, E, ED],
        to_node: N,
        get_node_data_func: Callable[
            [
                N,  # node ID
            ],
            Tuple[
                Optional[float],  # max weight of node
                Optional[E],      # edge ID of incoming edge made node have max weight
            ]
        ],
        get_edge_data_func: Callable[
            [
                E,  # edge ID
            ],
            Tuple[
                Tuple[Optional[ELEM], ...]  # elements
            ]
        ]
) -> List[List[Optional[ELEM]]]:
    node = to_node
    operations = []
    while True:
        weight, backtracking_edge = get_node_data_func(node)
        if backtracking_edge is None:
            break
        elements = get_edge_data_func(backtracking_edge)
        operations.insert(0, [elements, weight])
        node, _, _ = g.get_edge(backtracking_edge)

    seq_count = len(to_node)
    alignments = [[] for i in range(seq_count)]
    for op in operations:
        elements = op[0]
        for i, elem in enumerate(elements):
            alignments[i].append(elem)

    return alignments