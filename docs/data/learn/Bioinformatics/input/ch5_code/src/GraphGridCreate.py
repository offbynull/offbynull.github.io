import json
from itertools import product
from typing import TypeVar, List, Callable, Tuple, Optional

from Graph import Graph
from helpers.Utils import unique_id_generator

ELEM = TypeVar('ELEM')  # sequence element type
ND = TypeVar('ND')  # node data type
ED = TypeVar('ED')  # edge data type

ON_NEW_NODE_FUNC_TYPE =\
    Callable[
        [
            Tuple[int, ...]  # node id / coord
        ],
        Optional[ND]  # node data (may be None if flag is false)
    ]
ON_NEW_EDGE_FUNC_TYPE =\
    Callable[
        [
            Tuple[int, ...],  # src node id / coord
            Tuple[int, ...],  # dst node id / coord
            Tuple[int, ...],  # coord offsets (same as dst coord - src coord)
            Tuple[Optional[ELEM], ...]   # sequence elements at each coord
        ],
        Optional[ED]  # edge data (may be None if flag is false)
    ]


def create_grid_graph(
        sequences: List[List[ELEM]],
        on_new_node: ON_NEW_NODE_FUNC_TYPE,
        on_new_edge: ON_NEW_EDGE_FUNC_TYPE
) -> Graph[Tuple[int, ...], ND, str, ED]:
    create_edge_id_func = unique_id_generator('E')
    graph = Graph()
    axes = [[None] + av for av in sequences]
    axes_len = [range(len(axis)) for axis in axes]
    for grid_coord in product(*axes_len):
        node_data = on_new_node(grid_coord)
        if node_data is not None:
            graph.insert_node(grid_coord, node_data)
    for src_grid_coord in graph.get_nodes():
        for grid_coord_offsets in product([0, 1], repeat=len(sequences)):
            dst_grid_coord = tuple(axis + offset for axis, offset in zip(src_grid_coord, grid_coord_offsets))
            if src_grid_coord == dst_grid_coord:  # skip if making a connection to self
                continue
            if not graph.has_node(dst_grid_coord):  # skip if neighbouring node doesn't exist
                continue
            elements = tuple(None if src_idx == dst_idx else axes[axis_idx][dst_idx]
                             for axis_idx, (src_idx, dst_idx) in enumerate(zip(src_grid_coord, dst_grid_coord)))
            edge_data = on_new_edge(src_grid_coord, dst_grid_coord, grid_coord_offsets, elements)
            if edge_data is not None:
                edge_id = create_edge_id_func()
                graph.insert_edge(edge_id, src_grid_coord, dst_grid_coord, edge_data)
    return graph


def grid_graph_to_graphviz(graph: Graph[Tuple[int, ...], ND, str, ED]) -> str:
    dim = len(next(graph.get_nodes()))
    if dim < 2:
        raise ValueError('Need at least a dimension of 2')

    layers = set(n[:-2] for n in graph.get_nodes())
    row_len = max(n[-2] for n in graph.get_nodes()) + 1
    col_len = max(n[-1] for n in graph.get_nodes()) + 1
    dot_subgraph = 'digraph {\n'
    dot_subgraph += '  node [shape=plaintext]\n'
    for node_id_prefix in layers:
        dot_subgraph += f'  subgraph "cluster_{node_id_prefix}" {{\n'
        dot_subgraph += f'    label="{node_id_prefix}"\n'
        for node_id_suffix in product(range(row_len), range(col_len)):
            node_id = node_id_prefix + node_id_suffix
            if not graph.has_node(node_id):
                continue
            for edge_id in graph.get_outputs(node_id):
                child_node_id = graph.get_edge_to(edge_id)
                child_node_id_prefix = child_node_id[:-2]
                if child_node_id_prefix != node_id_prefix:
                    continue
                edge_data = graph.get_edge_data(edge_id)
                edge_label = json.dumps(edge_data).replace('"', '\\\"')
                dot_subgraph += f'    "{node_id}" -> "{child_node_id}"\n'
                # dot_subgraph += f'    "{node_id}" -> "{child_node_id}" [label="{edge_label}"]\n'
        for row in range(row_len):
            dot_subgraph += f'    rank=same {{ '
            dot_subgraph += ' '.join(f'"{node_id_prefix + (row, col)}"' for col in range(col_len))
            dot_subgraph += ' }\n'
        dot_subgraph += '  }\n'
    for node_id_prefix in layers:
        for node_id_suffix in product(range(row_len), range(col_len)):
            node_id = node_id_prefix + node_id_suffix
            if not graph.has_node(node_id):
                continue
            for edge_id in graph.get_outputs(node_id):
                child_node_id = graph.get_edge_to(edge_id)
                child_node_id_prefix = child_node_id[:-2]
                if child_node_id_prefix == node_id_prefix:
                    continue
                edge_data = graph.get_edge_data(edge_id)
                edge_label = json.dumps(edge_data).replace('"', '\\\"')
                dot_subgraph += f'  "{node_id}" -> "{child_node_id}"\n'
                # dot_subgraph += f'  "{node_id}" -> "{child_node_id}" [label="{edge_label}"]\n'
    dot_subgraph += '}'
    return dot_subgraph


if __name__ == '__main__':
    g = create_grid_graph(
        [
            list('HELLO'),
            list('YELLOW'),
            # list('TRELLO')
        ],
        lambda node_id: (),
        lambda src_id, dst_id, offsets, e: e
    )
    # print(f'{g}')
    print(f'{grid_graph_to_graphviz(g)}')