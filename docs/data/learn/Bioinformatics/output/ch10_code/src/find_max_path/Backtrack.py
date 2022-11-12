from typing import TypeVar, Callable, Tuple, Optional, List

from graph.Graph import Graph

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')
ED = TypeVar('ED')
ELEM = TypeVar('ELEM')

GET_NODE_DATA_FUNC_TYPE =\
    Callable[
        [
            N  # node ID
        ],
        Tuple[
            Optional[float],  # max weight of node
            Optional[E]       # edge ID of incoming edge made node have max weight
        ]
    ]
GET_EDGE_DATA_FUNC_TYPE =\
    Callable[
        [
            E  # edge ID
        ],
        Tuple[Optional[ELEM], ...]   # elements on edge (None if gap)
    ]
IS_FREE_RIDE_FUNC_TYPE =\
    Callable[
        [
            E  # edge ID
        ],
        bool
    ]


def backtrack(
        g: Graph[N, ND, E, ED],
        end_node: N,
        get_node_data_func: GET_NODE_DATA_FUNC_TYPE,
        get_edge_data_func: GET_EDGE_DATA_FUNC_TYPE,
        is_free_ride_func: IS_FREE_RIDE_FUNC_TYPE = lambda e: False,
) -> List[List[Optional[ELEM]]]:
    next_node = end_node
    column_elements = []
    while True:
        node = next_node
        weight, backtracking_edge = get_node_data_func(node)
        if backtracking_edge is None:
            break
        if is_free_ride_func(backtracking_edge):
            column_elements.insert(0, None)
        else:
            elements = get_edge_data_func(backtracking_edge)
            column_elements.insert(0, elements)

        next_node, _, _ = g.get_edge(backtracking_edge)

    seq_count = len(end_node)
    alignments = [[] for i in range(seq_count)]
    for elements in column_elements:
        if elements is None:
            continue
        for i, elem in enumerate(elements):
            alignments[i].append(elem)

    return alignments