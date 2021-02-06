import json
from itertools import product
from textwrap import dedent
from typing import List, Optional, TypeVar, Tuple, Callable, Set, Any

from FindMaxPath_DPBacktrack import populate_weights_and_backtrack_pointers, backtrack
from Graph import Graph
from GraphGridCreate import create_grid_graph
from WeightLookup import WeightLookup, Table2DWeightLookup
from helpers.Utils import latex_escape

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
def create_affine_gap_alignment_graph(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup,
        vertical_contig_gap_weight: float,
        horizontal_contig_gap_weight: float
) -> Graph[Tuple[int, ...], NodeData, str, EdgeData]:
    def on_new_node_func(n_id):
        return NodeData() if n_id[0] in {0, 1, 2} else None

    def on_new_edge_func(src_n_id, dst_n_id, offset, elems):
        # node id index 0 is the layer -- 0=low, 1=mid, 2=high
        if src_n_id[0] == 1 and dst_n_id == 1:
            return EdgeData(elems[1], elems[2], weight_lookup.lookup(*elems[1:3]))
        elif src_n_id[0] == 0 and dst_n_id[0] == 0:
            return EdgeData(elems[1], elems[2], vertical_contig_gap_weight) if offset[1:] == (1, 0) else None
        elif src_n_id[0] == 2 and dst_n_id[0] == 2:
            return EdgeData(elems[1], elems[2], horizontal_contig_gap_weight) if offset[1:] == (0, 1) else None
        elif src_n_id[0] == 1 and dst_n_id[0] == 0:
            return EdgeData(elems[1], elems[2], vertical_contig_gap_weight) if offset[1:] == (1, 0) else None
        elif src_n_id[0] == 1 and dst_n_id[0] == 2:
            return EdgeData(elems[1], elems[2], horizontal_contig_gap_weight) if offset[1:] == (0, 1) else None
        elif src_n_id[0] == 0 and dst_n_id[0] == 1:
            return EdgeData(elems[1], elems[2], 0.0) if offset[1:] == (1, 0) else None
        elif src_n_id[0] == 2 and dst_n_id[0] == 1:
            return EdgeData(elems[1], elems[2], 0.0) if offset[1:] == (0, 1) else None
        else:
            return None
    graph = create_grid_graph(
        [['low', 'mid', 'high'], v, w],
        on_new_node=on_new_node_func,
        on_new_edge=on_new_edge_func
    )
    return graph


def affine_gap_alignment(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup,
        vertical_contig_gap_weight: float,
        horizontal_contig_gap_weight: float
) -> Tuple[float, List[str], List[Tuple[ELEM, ELEM]]]:
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    graph = create_affine_gap_alignment_graph(v, w, weight_lookup, vertical_contig_gap_weight, horizontal_contig_gap_weight)
    from_node = (1, 0, 0)
    to_node = (1, v_node_count - 1, w_node_count - 1)
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























def graph_to_tikz(
        graph: Graph[Tuple[int, ...], NodeData, str, EdgeData],
        highlight_edges: Set[str],
        scale_x: float = 3.75,
        scale_y: float = 3.75
) -> str:
    layers = set(n[:-2] for n in graph.get_nodes())
    row_len = max(n[-2] for n in graph.get_nodes()) + 1
    col_len = max(n[-1] for n in graph.get_nodes()) + 1
    ret = dedent('''
    \\documentclass{standalone}
    \\usepackage{pgf, tikz, pagecolor}
    \\usetikzlibrary{arrows, automata}
    \\begin{document}
        \\pagecolor{white}
        \\begin{tikzpicture}
    ''')
    node_id_to_latex_id = {}
    for node_id_prefix in layers:
        for node_id_suffix in product(range(row_len), range(col_len)):
            node_id = node_id_prefix + node_id_suffix
            node_id_to_latex_id[node_id] = 'N' + '_'.join(str(c) for c in node_id)
        for node_id_suffix in product(range(row_len), range(col_len)):
            node_id = node_id_prefix + node_id_suffix
            node_data = graph.get_node_data(node_id)
            node_label = ''  # f'{node_id}'
            layer_pos_offset = {
                (2,): (0, -col_len * scale_x * 2),                      # high
                (1,): (row_len * scale_y * 1, -col_len * scale_x * 1),  # mid
                (0,): (row_len * scale_y * 2, 0)                        # low
            }[node_id_prefix]
            row_pos = node_id_suffix[0] * scale_x + layer_pos_offset[0]
            col_pos = -node_id_suffix[1] * scale_y + layer_pos_offset[1]
            ret += f'        \\node[draw = gray, fill = gray, thick, circle, minimum size = 2px] at ({row_pos}, {col_pos}) ({node_id_to_latex_id[node_id]}) {{{latex_escape(node_label)}}};\n'
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
                edge_color = 'gray!40'
                if edge_id in highlight_edges:
                    edge_color = 'green'
                edge_label = f'{"—" if edge_data.v_elem is None else edge_data.v_elem}\\\\ {"—" if edge_data.w_elem is None else edge_data.w_elem}\\\\ {edge_data.weight}'
                ret += f'        \\draw[->, >=stealth, line width = 2px, {edge_color}] ({node_id_to_latex_id[node_id]}) -- ({node_id_to_latex_id[child_node_id]}) node [align=center, midway, color=black] {{{edge_label}}};\n'
    ret += dedent('''
        \\end{tikzpicture}
    \\end{document}
    ''')
    return ret

























def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        s1 = list(input())
        s2 = list(input())
        matrix_type = input()
        indel_weight = float(input())
        vertical_contig_gap_weight, horizontal_contig_gap_weight = tuple(float(s.strip()) for s in input().split(','))
        if matrix_type == 'embedded_score_matrix':
            weights_data = ''
            try:
                while True:
                    weights_data += input() + '\n'
            except EOFError:
                ...
        elif matrix_type == 'file_score_matrix':
            path = input()
            with open(path, mode='r', encoding='utf-8') as f:
                weights_data = f.read()
        else:
            raise ValueError('Bad score matrix type')
        weight_lookup = Table2DWeightLookup.create_from_str(weights_data, indel_weight)
        weight, edges, elems = affine_gap_alignment(s1, s2, weight_lookup, vertical_contig_gap_weight, horizontal_contig_gap_weight)
        graph = create_affine_gap_alignment_graph(s1, s2, weight_lookup, vertical_contig_gap_weight, horizontal_contig_gap_weight)
        output = graph_to_tikz(
            graph,
            set(edges)
        )
        print(f'Given the sequences {"".join(s1)} and {"".join(s2)} and the score matrix...', end="\n\n")
        print(f'```\nINDEL={indel_weight}\n{weights_data}\n````', end="\n\n")
        print(f'... the global alignment is...', end="\n\n")
        print(f'````{{latex}}\n{output}\n````', end='\n\n')
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
