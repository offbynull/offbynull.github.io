from typing import TypeVar, Callable, Tuple, Optional

from Graph import Graph

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')
ED = TypeVar('ED')
ELEMENT = TypeVar('ELEMENT')

def backtrack(
        g: Graph[N, ND, E, ED],
        to_node: N,
        get_node_data_func: Callable[
            [
                N,  # node ID
            ],
            Tuple[
                Optional[float],  # max weight of node
                E,  # edge ID of incoming edge made node have max weight
            ]
        ],
        get_edge_data_func: Callable[
            [
                E,  # edge ID
            ],
            Tuple[
                Tuple[Optional[ELEMENT], ...]  # elements
            ]
        ]
):
    # Now backtrack from the end_node to start_node to get the path.
    node = to_node
    operations = []
    while True:
        weight, backtracking_edge = get_node_data_func(node)
        if backtracking_edge is None:
            break
        elements = get_edge_data_func(backtracking_edge)
        operations.insert(0, [elements, weight])
        node, _, _ = g.get_edge(backtracking_edge)

    # print(f'{operations}')
    # print(f'{g}')

    seq_count = len(operations[0][0])
    alignments = [[] * seq_count]
    for op in operations:
        elements = op[0]
        for i, elem in enumerate(elements):
            alignments[i] = elem if elem is not None else '-'

    for alignment in alignments:
        print(alignment)


    # for elements, weight in operations:
    #     for`
    #     if op == ModificationType.KEEP_S1_ONLY:
    #         _, _, s1_ch, s2_ch = g.get_node_data(node)
    #         s1_alignment.append(s1_ch)
    #         s2_alignment.append('-')
    #     elif op == ModificationType.KEEP_S2_ONLY:
    #         _, _, s1_ch, s2_ch = g.get_node_data(node)
    #         s1_alignment.append('-')
    #         s2_alignment.append(s2_ch)
    #     elif op == ModificationType.KEEP_BOTH:
    #         _, _, s1_ch, s2_ch = g.get_node_data(node)
    #         s1_alignment.append(s1_ch)
    #         s2_alignment.append(s2_ch)
    #     elif op == ModificationType.SKIP:
    #         continue  # do nothing -- this is a free ride to the starting point