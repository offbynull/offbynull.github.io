import json
from itertools import product
from typing import Tuple, TypeVar, Callable, Any

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


def grid_graph_to_graphviz(
        graph: Graph[Tuple[int, ...], Any, str, Any],
        get_node_label_func=lambda nd: json.dumps(nd).replace('"', '\\\"'),
        get_edge_label_func=lambda ed: json.dumps(ed).replace('"', '\\\"'),
        scale_x: int = 1,
        scale_y: int = 1
) -> str:
    dim = len(next(graph.get_nodes()))
    if dim < 2:
        raise ValueError('Need at least a dimension of 2')

    layers = set(n[:-2] for n in graph.get_nodes())
    row_len = max(n[-2] for n in graph.get_nodes()) + 1
    col_len = max(n[-1] for n in graph.get_nodes()) + 1
    dot_subgraph = 'digraph {\n'
    dot_subgraph += '  node[shape=point, fontname="Courier-Bold", fontsize=10]\n'
    dot_subgraph += '  edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10]\n'
    for node_id_prefix in layers:
        dot_subgraph += f'  subgraph "cluster_{node_id_prefix}" {{\n'
        dot_subgraph += f'    label="{node_id_prefix}"\n'
        for node_id_suffix in product(range(row_len), range(col_len)):
            node_id = node_id_prefix + node_id_suffix
            node_data = graph.get_node_data(node_id)
            node_label = get_node_label_func(node_data)
            row_pos = node_id_suffix[0] * scale_x
            col_pos = -node_id_suffix[1] * scale_y
            dot_subgraph += f'    "{node_id}" [label="{node_label}", pos="{row_pos},{col_pos}!"]\n'
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
                edge_label = get_edge_label_func(edge_data)
                dot_subgraph += f'    "{node_id}" -> "{child_node_id}" [label="{edge_label}"]\n'
        dot_subgraph += '  }\n'
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
    output = grid_graph_to_graphviz(g, scale_x=1.5, scale_y=1.5,
                                    get_edge_label_func=lambda e: "\\n".join(["-" if ch is None else ch for ch in e]),
                                    get_node_label_func=lambda n: "")
    print(f'{output}')  # render with fdp, not dot