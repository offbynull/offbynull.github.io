import json
from itertools import product
from typing import List, Optional, TypeVar, Tuple, Callable

from FindMaxPath_DPBacktrack import populate_weights_and_backtrack_pointers, backtrack
from Graph import Graph
from GraphGridCreate import create_grid_graph
from WeightLookup import WeightLookup, Constant2DWeightLookup

ELEM = TypeVar('ELEM')

class NodeData:
    def __init__(self):
        self.weight = None
        self.backtracking_edge = None

    def set_weight_and_backtracking_edge(self, weight: float, backtracking_edge: str):
        self.weight = weight
        self.backtracking_edge = backtracking_edge

    def get_weight_and_backtracking_edge(self):
        return self.weight, self.backtracking_edge


class EdgeData:
    def __init__(self, v_elem: Optional[ELEM], w_elem: Optional[ELEM], weight: float):
        self.v_elem = v_elem
        self.w_elem = w_elem
        self.weight = weight

    def get_elements(self) -> Tuple[Optional[ELEM], Optional[ELEM]]:
        return self.v_elem, self.w_elem


# MARKDOWN
def create_global_alignment_graph(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup
) -> Graph[Tuple[int, ...], NodeData, str, EdgeData]:
    graph = create_grid_graph(
        [v, w],
        lambda n_id: NodeData(),
        lambda src_n_id, dst_n_id, offset, elems: EdgeData(elems[0], elems[1], weight_lookup.lookup(*elems))
    )
    return graph


def global_alignment(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup
) -> Tuple[float, List[str], List[Tuple[ELEM, ELEM]]]:
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    graph = create_global_alignment_graph(v, w, weight_lookup)
    from_node = (0, 0)
    to_node = (v_node_count - 1, w_node_count - 1)
    populate_weights_and_backtrack_pointers(
        graph,
        from_node,
        lambda n_id, weight, e_id: graph.get_node_data(n_id).set_weight_and_backtracking_edge(weight, e_id),
        lambda n_id: graph.get_node_data(n_id).get_weight_and_backtracking_edge(),
        lambda e_id: graph.get_edge_data(e_id).weight
    )
    final_weight = graph.get_node_data(to_node).weight
    edges = backtrack(
        graph,
        to_node,
        lambda n_id: graph.get_node_data(n_id).get_weight_and_backtracking_edge()
    )
    alignment = []
    for e in edges:
        ed = graph.get_edge_data(e)
        alignment.append((ed.v_elem, ed.w_elem))
    return final_weight, edges, alignment
# MARKDOWN






















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

IS_EDGE_HIGHLIGHT_FUNC_TYPE =\
    Callable[
        [
            E
        ],
        bool
    ]

def graph_to_graphviz(
        graph: Graph[N, ND, E, ED],
        get_node_label_func: GET_NODE_LABEL_FUNC_TYPE = lambda nd: json.dumps(nd).replace('"', '\\\"'),
        get_edge_label_func: GET_EDGE_LABEL_FUNC_TYPE = lambda ed: json.dumps(ed).replace('"', '\\\"'),
        is_edge_highlight_func: IS_EDGE_HIGHLIGHT_FUNC_TYPE = lambda e: False,
        scale_x: float = 1.5,
        scale_y: float = 1.5
) -> str:
    dim = len(next(graph.get_nodes()))
    if dim < 2:
        raise ValueError('Need at least a dimension of 2')
    layers = set(n[:-2] for n in graph.get_nodes())
    row_len = max(n[-2] for n in graph.get_nodes()) + 1
    col_len = max(n[-1] for n in graph.get_nodes()) + 1
    dot_subgraph = 'digraph {\n'
    dot_subgraph += '  node[shape=point, width=0.15, color="grey", fontname="Courier", fontsize=10]\n'
    dot_subgraph += '  edge[color="grey", penwidth=2, fontname="Courier", fontsize=10]\n'
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
                dot_subgraph += f', color="green"' if is_edge_highlight_func(edge_id) else ''
                dot_subgraph += f']\n'
        dot_subgraph += '  }\n'
    dot_subgraph += '}'
    return dot_subgraph


























def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        s1 = list(input())
        s2 = list(input())
        weight_lookup = Constant2DWeightLookup(1.0, 0.0, -1.0)
        weight, edges, elems = global_alignment(s1, s2, weight_lookup)
        graph = create_global_alignment_graph(s1, s2, weight_lookup)
        output = graph_to_graphviz(
            graph,
            get_edge_label_func=lambda ed: f'{"-" if ed.v_elem is None else ed.v_elem}\n{"-" if ed.w_elem is None else ed.w_elem}\n{ed.weight}',
            is_edge_highlight_func=lambda e: e.startswith('E') and e in edges,
            get_node_label_func=lambda nd: "",
            scale_x=1.75,
            scale_y=1.75
        )
        print(f'Given the sequences {"".join(s1)} and {"".join(s2)}, the global alignment is...', end="\n\n")
        print(f'````{{graphvizFdp}}\n{output}\n````', end='\n\n')
        print(f'````')
        print(f'{"".join("-" if e[0] is None else e[0] for e in elems)}')
        print(f'{"".join("-" if e[1] is None else e[1] for e in elems)}')
        print(f'````', end='\n\n')
        print(f'Weight: {weight}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
