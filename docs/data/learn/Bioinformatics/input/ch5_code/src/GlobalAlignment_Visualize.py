import json
from itertools import product
from typing import Tuple, TypeVar, Callable, Any, Set

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

GET_NODE_LABEL_FUNC_TYPE =\
    Callable[
        [
            ND
        ],
        str
    ]

def graph_to_graphviz(
        graph: Graph[Tuple[int, ...], Any, str, Any],
        get_node_label_func: GET_NODE_LABEL_FUNC_TYPE = lambda nd: json.dumps(nd).replace('"', '\\\"'),
        get_edge_label_func: GET_NODE_LABEL_FUNC_TYPE = lambda ed: json.dumps(ed).replace('"', '\\\"'),
        scale_x: float = 1.0,
        scale_y: float = 1.0,
        edge_highlights: Set[Tuple[Tuple[int, ...], Tuple[int, ...]]] = ()
) -> str:
    dim = len(next(graph.get_nodes()))
    if dim < 2:
        raise ValueError('Need at least a dimension of 2')

    layers = set(n[:-2] for n in graph.get_nodes())
    row_len = max(n[-2] for n in graph.get_nodes()) + 1
    col_len = max(n[-1] for n in graph.get_nodes()) + 1
    dot_subgraph = 'digraph {\n'
    dot_subgraph += '  node[shape=point]\n'
    dot_subgraph += '  edge[]\n'
    for node_id_prefix in layers:
        dot_subgraph += f'  subgraph "cluster_{node_id_prefix}" {{\n'
        dot_subgraph += f'    style=invis\n'
        # dot_subgraph += f'    label="{node_id_prefix}"\n'
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
                dot_subgraph += f'    "{node_id}" -> "{child_node_id}" [label="{edge_label}"'
                dot_subgraph += f', color="green"' if (node_id, child_node_id) in edge_highlights else ''
                dot_subgraph += f']\n'
        dot_subgraph += '  }\n'
    dot_subgraph += '}'
    return dot_subgraph


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        s1 = input()
        s2 = input()
        try:
            edge_highlights = {tuple((int(t.split(',')[1]), int(t.split(',')[0])) for t in s.split('->')) for s in input().split('|')}  # 0,0->1,1|0,0->0,1
        except EOFError:
            edge_highlights = set()

        graph = create_grid_graph(
            [
                list(s1),
                list(s2)
            ],
            lambda node_id: (),
            lambda src_id, dst_id, offsets, e: e
        )
        output = graph_to_graphviz(
            graph,
            get_edge_label_func=lambda e: "\\n".join(["-" if ch is None else ch for ch in e]),
            get_node_label_func=lambda n: "",
            scale_x=1.5,
            scale_y=1.5,
            edge_highlights=edge_highlights
        )
        print(f'````{{graphvizFdp}}\n{output}\n````', end='\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()