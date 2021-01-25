import json
from itertools import product
from typing import Tuple, TypeVar, Callable

from Graph import Graph
from GraphGridCreate import create_grid_graph

ELEM = TypeVar('ELEM')  # sequence element type
N = TypeVar('N')  # node id
ND = TypeVar('ND')  # node data type
E = TypeVar('E')  # edge id
ED = TypeVar('ED')  # edge data type

GET_EDGE_LABEL_FUNC_TYPE =\
    Callable[
        [
            ED
        ],
        str
    ]



def graph_to_graphviz(
        graph: Graph[N, ND, E, ED],
        get_edge_label_func: GET_EDGE_LABEL_FUNC_TYPE
) -> str:
    dot_subgraph = 'digraph {\n'
    dot_subgraph += '  node [shape=plaintext]\n'
    for node_id in graph.get_nodes():
        dot_subgraph += f'  "{node_id}"\n'
    for edge_id in graph.get_edges():
        from_id, to_id, data = graph.get_edge(edge_id)
        label = get_edge_label_func(data)
        dot_subgraph += f'  "{from_id}" -> "{to_id}" [label="{label}"]\n'
    dot_subgraph += '}'
    return dot_subgraph


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
            list('TRELLO')
        ],
        lambda node_id: (),
        lambda src_id, dst_id, offsets, e: e
    )
    # print(f'{g}')
    print(f'{graph_to_graphviz(g, lambda e: str(e))}')