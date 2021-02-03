from itertools import product
from typing import List, Optional, TypeVar, Tuple, Set

from FindMaxPath_DPBacktrack import populate_weights_and_backtrack_pointers, backtrack
from Graph import Graph
from GraphGridCreate import create_grid_graph
from WeightLookup import WeightLookup, Table2DWeightLookup
from helpers.Utils import unique_id_generator

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
        self.weight = weight
        self.v_elem = v_elem
        self.w_elem = w_elem

    def get_elements(self) -> Tuple[Optional[ELEM], Optional[ELEM]]:
        return self.v_elem, self.w_elem


# MARKDOWN
def create_fitting_alignment_graph(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup
) -> Graph[Tuple[int, ...], NodeData, str, EdgeData]:
    graph = create_grid_graph(
        [v, w],
        lambda n_id: NodeData(),
        lambda src_n_id, dst_n_id, offset, elems: EdgeData(elems[0], elems[1], weight_lookup.lookup(*elems))
    )
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    source_node = 0, 0
    source_create_free_ride_edge_id_func = unique_id_generator('FREE_RIDE_SOURCE')
    for node in product([0], range(w_node_count)):
        if node == source_node:
            continue
        e = source_create_free_ride_edge_id_func()
        graph.insert_edge(e, source_node, node, EdgeData(None, None, 0.0))
    sink_node = v_node_count - 1, w_node_count - 1
    sink_create_free_ride_edge_id_func = unique_id_generator('FREE_RIDE_SINK')
    for node in product([v_node_count - 1], range(w_node_count)):
        if node == sink_node:
            continue
        e = sink_create_free_ride_edge_id_func()
        graph.insert_edge(e, node, sink_node, EdgeData(None, None, 0.0))
    return graph


def fitting_alignment(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup
) -> Tuple[float, List[str], List[Tuple[ELEM, ELEM]]]:
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    graph = create_fitting_alignment_graph(v, w, weight_lookup)
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
    edges = list(filter(lambda e: not e.startswith('FREE_RIDE'), edges))  # remove free rides from list
    alignment = []
    for e in edges:
        ed = graph.get_edge_data(e)
        alignment.append((ed.v_elem, ed.w_elem))
    return final_weight, edges, alignment
# MARKDOWN






















def graph_to_graphviz(
        graph: Graph[Tuple[int, ...], NodeData, str, EdgeData],
        highlight_edges: Set[str],
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
    dot_subgraph += '  splines="curved"\n'  # ALL EDGES WILL BE CURVED -- so far I haven't found a way to keep free rides curved but normal edges straight
    dot_subgraph += '  node[shape=point, width=0.15, color="grey", fontname="Courier", fontsize=10]\n'
    dot_subgraph += '  edge[color="grey", penwidth=2, fontname="Courier", fontsize=10]\n'
    for node_id_prefix in layers:
        dot_subgraph += f'  subgraph "cluster_{node_id_prefix}" {{\n'
        dot_subgraph += f'    style=invis\n'
        # dot_subgraph += f'    label="{node_id_prefix}"\n'
        for node_id_suffix in product(range(row_len), range(col_len)):
            node_id = node_id_prefix + node_id_suffix
            node_data = graph.get_node_data(node_id)
            node_label = ''  # f'{node_id}'
            row_pos = node_id_suffix[0] * scale_x
            col_pos = -node_id_suffix[1] * scale_y
            dot_subgraph += f'    "{node_id}" [label="{node_label}", pos="{row_pos},{col_pos}!"]\n'
        for node_id_suffix in product(range(row_len), range(col_len)):
            node_id = node_id_prefix + node_id_suffix
            if not graph.has_node(node_id):
                continue
            edge_ids = list(graph.get_outputs(node_id))
            edge_ids.sort()  # E goes first, then the FREE_RIDE edges
            for edge_id in edge_ids:
                child_node_id = graph.get_edge_to(edge_id)
                child_node_id_prefix = child_node_id[:-2]
                if child_node_id_prefix != node_id_prefix:
                    continue
                edge_data = graph.get_edge_data(edge_id)
                edge_params = {}
                post_from = ''
                port_to = ''
                if edge_id.startswith('FREE_RIDE_SOURCE'):
                    edge_params['color'] = 'orange'
                    edge_params['penwidth'] = '1'
                    post_from = ':nw'
                    port_to = ':w'
                if edge_id.startswith('FREE_RIDE_SINK'):
                    edge_params['color'] = 'purple'
                    edge_params['penwidth'] = '1'
                    post_from = ':se'
                    port_to = ':e'
                if edge_id in highlight_edges:
                    edge_params['color'] = 'green'
                if edge_id.startswith('E'):
                    edge_params['label'] = f'{"-" if edge_data.v_elem is None else edge_data.v_elem}\n{"-" if edge_data.w_elem is None else edge_data.w_elem}\n{edge_data.weight}'
                dot_subgraph += f'    "{node_id}"{post_from} -> "{child_node_id}"{port_to} [' + ', '.join(f'{k}="{v}"' for k, v in edge_params.items()) + ']\n'
        dot_subgraph += '  }\n'
    dot_subgraph += '}'
    return dot_subgraph


























def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        s1 = list(input())
        s2 = list(input())
        matrix_type = input()
        if matrix_type == 'embedded_score_matrix':
            indel_weight = float(input())
            weights_data = ''
            try:
                while True:
                    weights_data += input() + '\n'
            except EOFError:
                ...
        elif matrix_type == 'file_score_matrix':
            indel_weight = float(input())
            path = input()
            with open(path, mode='r', encoding='utf-8') as f:
                weights_data = f.read()
        else:
            raise ValueError('Bad score matrix type')
        weight_lookup = Table2DWeightLookup.create_from_str(weights_data, indel_weight)
        weight, edges, elems = fitting_alignment(s1, s2, weight_lookup)
        graph = create_fitting_alignment_graph(s1, s2, weight_lookup)
        output = graph_to_graphviz(
            graph,
            set(edges),
            scale_x=1.75,
            scale_y=1.75
        )
        print(f'Given the sequences {"".join(s1)} and {"".join(s2)} and the score matrix...', end="\n\n")
        print(f'```\nINDEL={indel_weight}\n{weights_data}\n````', end="\n\n")
        print(f'... the global alignment is...', end="\n\n")
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
